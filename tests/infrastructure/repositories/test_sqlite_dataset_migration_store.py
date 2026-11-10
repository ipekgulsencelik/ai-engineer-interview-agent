"""SQLite transaction, audit, rollback and recovery integration tests."""

from __future__ import annotations

import logging
import sqlite3

import pytest

from src.evaluation.dataset.schema_evolution import (
    DatasetField,
    DatasetRecordSchema,
    MigrationRegistry,
    MigrationStep,
    RenameField,
    SchemaEvolutionError,
    SchemaEvolutionService,
    SetDefault,
)
from src.evaluation.dataset.schema_evolution.coordinator import (
    DatasetMigrationCoordinator,
)
from src.infrastructure.logging.dataset_migration_telemetry import (
    LoggingDatasetMigrationTelemetry,
)
from src.infrastructure.repositories.sqlite_dataset_migration_store import (
    SQLiteDatasetMigrationStore,
)
from src.infrastructure.repositories.sqlite_dataset_schema_repository import (
    SQLiteDatasetSchemaRepository,
)


def _commit(store: SQLiteDatasetMigrationStore) -> None:
    store.commit_migration(
        schema_name="interviews",
        source_version="1.0.0",
        target_version="2.0.0",
        source_records=[{"old": "private raw answer"}],
        target_records=[{"new": "private raw answer"}],
    )


def test_commit_persists_snapshot_and_durable_audit_across_restarts(
    tmp_path,
) -> None:
    path = tmp_path / "migrations.sqlite"
    store = SQLiteDatasetMigrationStore(path)
    _commit(store)
    reopened = SQLiteDatasetMigrationStore(path)

    snapshot = reopened.current_snapshot(schema_name="interviews")
    assert snapshot is not None
    assert snapshot.schema_version == "2.0.0"
    assert snapshot.records == ({"new": "private raw answer"},)

    audit = reopened.audit_events(schema_name="interviews")
    assert len(audit) == 1
    assert audit[0].operation == "migration"
    assert audit[0].record_count == 1
    assert audit[0].source_hash != audit[0].target_hash
    assert audit[0].target_hash == snapshot.checksum


def test_rollback_restores_original_snapshot_and_audits_action(tmp_path) -> None:
    store = SQLiteDatasetMigrationStore(tmp_path / "migrations.sqlite")
    _commit(store)
    rollback = store.rollback_last(schema_name="interviews")
    assert rollback.operation == "rollback"
    assert rollback.source_version == "2.0.0"
    assert rollback.target_version == "1.0.0"

    current = store.current_snapshot(schema_name="interviews")
    assert current is not None
    assert current.schema_version == "1.0.0"
    assert current.records == ({"old": "private raw answer"},)
    assert tuple(entry.operation for entry in store.audit_events(
        schema_name="interviews"
    )) == ("migration", "rollback")
    with pytest.raises(SchemaEvolutionError, match="no migration"):
        store.rollback_last(schema_name="interviews")


def test_multiple_versions_rollback_only_the_latest_snapshot(tmp_path) -> None:
    store = SQLiteDatasetMigrationStore(tmp_path / "migrations.sqlite")
    _commit(store)
    store.commit_migration(
        schema_name="interviews",
        source_version="2.0.0",
        target_version="3.0.0",
        source_records=[{"new": "private raw answer"}],
        target_records=[{"answer": "private raw answer"}],
    )
    store.rollback_last(schema_name="interviews")
    snapshot = store.current_snapshot(schema_name="interviews")
    assert snapshot is not None
    assert snapshot.schema_version == "2.0.0"
    assert snapshot.records == ({"new": "private raw answer"},)


def test_stale_source_is_rejected_without_changing_active_snapshot(
    tmp_path,
) -> None:
    store = SQLiteDatasetMigrationStore(tmp_path / "migrations.sqlite")
    _commit(store)
    original = store.current_snapshot(schema_name="interviews")
    with pytest.raises(SchemaEvolutionError, match="active dataset differs"):
        store.commit_migration(
            schema_name="interviews",
            source_version="1.0.0",
            target_version="3.0.0",
            source_records=[{"old": "outdated"}],
            target_records=[{"new": "incorrect"}],
        )
    assert store.current_snapshot(schema_name="interviews") == original
    assert len(store.audit_events(schema_name="interviews")) == 1


def test_audit_insertion_failure_rolls_back_all_snapshot_writes(tmp_path) -> None:
    path = tmp_path / "migrations.sqlite"
    store = SQLiteDatasetMigrationStore(path)
    with sqlite3.connect(path) as conn:
        conn.execute(
            """
            CREATE TRIGGER reject_audit BEFORE INSERT ON dataset_migration_audit
            BEGIN SELECT RAISE(ABORT, 'injected audit failure'); END
            """
        )
    with pytest.raises(SchemaEvolutionError, match="transaction failed"):
        _commit(store)
    assert store.current_snapshot(schema_name="interviews") is None
    assert store.audit_events(schema_name="interviews") == ()
    with sqlite3.connect(path) as conn:
        count = conn.execute(
            "SELECT COUNT(*) FROM dataset_migration_snapshots"
        ).fetchone()[0]
    assert count == 0


def test_rollback_audit_failure_does_not_move_current_head(tmp_path) -> None:
    path = tmp_path / "migrations.sqlite"
    store = SQLiteDatasetMigrationStore(path)
    _commit(store)
    before = store.current_snapshot(schema_name="interviews")
    with sqlite3.connect(path) as conn:
        conn.execute(
            """
            CREATE TRIGGER reject_rollback BEFORE INSERT
            ON dataset_migration_audit
            WHEN NEW.operation = 'rollback'
            BEGIN SELECT RAISE(ABORT, 'injected rollback failure'); END
            """
        )
    with pytest.raises(SchemaEvolutionError, match="rollback transaction"):
        store.rollback_last(schema_name="interviews")
    assert store.current_snapshot(schema_name="interviews") == before


def test_store_rejects_record_loss_and_non_serializable_records(tmp_path) -> None:
    store = SQLiteDatasetMigrationStore(tmp_path / "migrations.sqlite")
    with pytest.raises(SchemaEvolutionError, match="preserve record count"):
        store.commit_migration(
            schema_name="interviews",
            source_version="1.0.0",
            target_version="1.1.0",
            source_records=[{"id": 1}],
            target_records=[],
        )
    with pytest.raises(SchemaEvolutionError, match="JSON-serializable"):
        store.commit_migration(
            schema_name="interviews",
            source_version="1.0.0",
            target_version="1.1.0",
            source_records=[{"secret": object()}],
            target_records=[{"secret": "valid"}],
        )
    with pytest.raises(SchemaEvolutionError, match="must increase"):
        store.commit_migration(
            schema_name="interviews",
            source_version="2.0.0",
            target_version="1.0.0",
            source_records=[],
            target_records=[],
        )
    assert store.current_snapshot(schema_name="interviews") is None


def test_tampered_snapshot_is_detected_by_checksum(tmp_path) -> None:
    path = tmp_path / "migrations.sqlite"
    store = SQLiteDatasetMigrationStore(path)
    _commit(store)
    with sqlite3.connect(path) as conn:
        conn.execute(
            """
            UPDATE dataset_migration_snapshots SET records_json = '[]'
            WHERE schema_version = '2.0.0'
            """
        )
    with pytest.raises(SchemaEvolutionError, match="checksum mismatch"):
        store.current_snapshot(schema_name="interviews")


def test_coordinator_runs_end_to_end_using_persisted_intermediate_schema(
    tmp_path,
) -> None:
    path = tmp_path / "workflow.sqlite"
    registry = SQLiteDatasetSchemaRepository(path)
    source = DatasetRecordSchema(
        name="interviews",
        version="1.0.0",
        fields=(DatasetField("old", "string"),),
    )
    intermediate = DatasetRecordSchema(
        name="interviews",
        version="1.1.0",
        fields=(
            DatasetField("old", "string"),
            DatasetField("status", "string"),
        ),
    )
    target = DatasetRecordSchema(
        name="interviews",
        version="2.0.0",
        fields=(
            DatasetField("answer", "string"),
            DatasetField("status", "string"),
        ),
    )
    for schema in (source, intermediate, target):
        registry.register(schema=schema)
    store = SQLiteDatasetMigrationStore(path)
    service = SchemaEvolutionService(
        migrations=MigrationRegistry(
            (
                MigrationStep(
                    "1.0.0", "1.1.0", (SetDefault("status", "ready"),)
                ),
                MigrationStep(
                    "1.1.0", "2.0.0", (RenameField("old", "answer"),)
                ),
            )
        ),
        intermediate_schemas=registry,
    )
    coordinator = DatasetMigrationCoordinator(
        migrator=service,
        persistence=store,
        telemetry=LoggingDatasetMigrationTelemetry(
            logging.getLogger("dataset.integration-test")
        ),
    )
    result = coordinator.execute(
        records=[{"old": "test answer"}],
        source_schema=registry.get_schema(
            name="interviews", version="1.0.0"
        ),
        target_schema=registry.get_schema(
            name="interviews", version="2.0.0"
        ),
    )
    assert result.operation == "migration"
    snapshot = store.current_snapshot(schema_name="interviews")
    assert snapshot is not None
    assert snapshot.records == (
        {"answer": "test answer", "status": "ready"},
    )
    coordinator.rollback_last(schema_name="interviews")
    restored = store.current_snapshot(schema_name="interviews")
    assert restored is not None
    assert restored.records == ({"old": "test answer"},)
    assert len(store.audit_events(schema_name="interviews")) == 2


def test_structured_telemetry_exposes_metadata_not_raw_records(
    tmp_path, caplog: pytest.LogCaptureFixture
) -> None:
    store = SQLiteDatasetMigrationStore(tmp_path / "migrations.sqlite")
    event = store.commit_migration(
        schema_name="interviews",
        source_version="1.0.0",
        target_version="1.1.0",
        source_records=[{"answer": "sensitive text"}],
        target_records=[{"answer": "sensitive text"}],
    )
    logger = logging.getLogger("dataset.schema.telemetry.test")
    with caplog.at_level(logging.INFO, logger=logger.name):
        LoggingDatasetMigrationTelemetry(logger).publish(event)
    assert "sensitive text" not in caplog.text
    assert "migration" in caplog.text
    record = caplog.records[-1]
    assert getattr(record, "migration_event_id") == event.event_id
    assert getattr(record, "migration_record_count") == 1
