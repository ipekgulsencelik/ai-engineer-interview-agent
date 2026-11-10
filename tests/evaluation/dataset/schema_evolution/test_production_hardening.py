"""Regression and failure-mode tests for hardened schema evolution."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from src.evaluation.dataset.schema_evolution import (
    DatasetField,
    DatasetRecordSchema,
    DatasetRecordValidator,
    MigrationRegistry,
    MigrationStep,
    RenameField,
    SchemaCompatibilityChecker,
    SchemaEvolutionError,
    SchemaEvolutionService,
    SetDefault,
)
from src.evaluation.dataset.schema_evolution.coordinator import (
    DatasetMigrationCoordinator,
)
from src.evaluation.dataset.schema_evolution.persistence import (
    MigrationAuditEvent,
)


def _nested(version: str = "1.0.0") -> DatasetRecordSchema:
    return DatasetRecordSchema(
        name="interviews",
        version=version,
        fields=(
            DatasetField("id", "string"),
            DatasetField(
                "profile",
                "object",
                properties=(
                    DatasetField("age", "integer"),
                    DatasetField("nickname", "string", required=False),
                ),
            ),
            DatasetField(
                "scores",
                "array",
                items=DatasetField(
                    "score",
                    "object",
                    properties=(
                        DatasetField("value", "number"),
                        DatasetField("passed", "boolean"),
                    ),
                ),
            ),
        ),
    )


def _record() -> dict[str, object]:
    return {
        "id": "abc",
        "profile": {"age": 18},
        "scores": [{"value": 0.8, "passed": True}],
    }


def test_nested_schema_validates_objects_and_array_items() -> None:
    DatasetRecordValidator().validate(schema=_nested(), record=_record())


@pytest.mark.parametrize(
    "mutation,field",
    [
        ({"profile": {"age": "18"}}, "profile.age"),
        ({"profile": {}}, "profile.age"),
        ({"profile": {"age": 18, "unknown": 1}}, "profile"),
        ({"scores": [{"value": "0.8", "passed": True}]}, "scores[0].value"),
        ({"scores": [{"value": 0.8, "passed": 1}]}, "scores[0].passed"),
        ({"scores": [None]}, "scores[0]"),
    ],
)
def test_nested_schema_rejects_invalid_nested_values(
    mutation: dict[str, object], field: str
) -> None:
    record = _record()
    record.update(mutation)
    with pytest.raises(SchemaEvolutionError, match=r".+"):
        DatasetRecordValidator().validate(schema=_nested(), record=record)
    # The record location should be included in error messages.
    try:
        DatasetRecordValidator().validate(schema=_nested(), record=record)
    except SchemaEvolutionError as exc:
        assert field in str(exc)


def test_nested_schema_checks_invalid_field_definitions() -> None:
    with pytest.raises(SchemaEvolutionError, match="only object"):
        DatasetField(
            "bad", "string", properties=(DatasetField("x", "string"),)
        )
    with pytest.raises(SchemaEvolutionError, match="duplicate nested"):
        DatasetField(
            "bad",
            "object",
            properties=(
                DatasetField("x", "string"),
                DatasetField("x", "boolean"),
            ),
        )
    with pytest.raises(SchemaEvolutionError, match="only arrays"):
        DatasetField("bad", "integer", items=DatasetField("i", "string"))


def test_nested_compatibility_reports_breaking_child_changes() -> None:
    old = _nested()
    new = DatasetRecordSchema(
        name="interviews",
        version="2.0.0",
        fields=(
            DatasetField("id", "string"),
            DatasetField(
                "profile",
                "object",
                properties=(DatasetField("age", "number"),),
            ),
            DatasetField(
                "scores",
                "array",
                items=DatasetField(
                    "item",
                    "object",
                    properties=(
                        DatasetField("value", "number"),
                        DatasetField("passed", "boolean"),
                    ),
                ),
            ),
        ),
    )
    report = SchemaCompatibilityChecker().compare(source=old, target=new)
    assert not report.backward_compatible
    assert "changed type: profile.age" in report.breaking_changes


def test_nested_compatibility_relaxation_is_backward_compatible() -> None:
    old = DatasetRecordSchema(
        name="test",
        version="1.0.0",
        fields=(
            DatasetField(
                "profile",
                "object",
                properties=(DatasetField("age", "integer"),),
            ),
        ),
    )
    new = DatasetRecordSchema(
        name="test",
        version="1.1.0",
        fields=(DatasetField("profile", "object"),),
    )
    assert SchemaCompatibilityChecker().compare(
        source=old, target=new
    ).backward_compatible


class _IntermediateSchemas:
    def __init__(self, schema: DatasetRecordSchema) -> None:
        self.schema = schema
        self.lookups: list[tuple[str, str]] = []

    def get_schema(self, *, name: str, version: str) -> DatasetRecordSchema:
        self.lookups.append((name, version))
        return self.schema


def _step_schemas() -> tuple[
    DatasetRecordSchema,
    DatasetRecordSchema,
    DatasetRecordSchema,
]:
    source = DatasetRecordSchema(
        "steps", "1.0.0", (DatasetField("id", "string"),)
    )
    middle = DatasetRecordSchema(
        "steps", "1.1.0", (
            DatasetField("id", "string"),
            DatasetField("status", "string"),
        )
    )
    target = DatasetRecordSchema(
        "steps", "2.0.0", (
            DatasetField("id", "string"),
            DatasetField("state", "string"),
        )
    )
    return source, middle, target


def test_validated_intermediate_steps_succeed() -> None:
    source, middle, target = _step_schemas()
    lookup = _IntermediateSchemas(middle)
    migrations = MigrationRegistry(
        (
            MigrationStep("1.0.0", "1.1.0", (SetDefault("status", "ok"),)),
            MigrationStep("1.1.0", "2.0.0", (RenameField("status", "state"),)),
        )
    )
    result = SchemaEvolutionService(
        migrations=migrations, intermediate_schemas=lookup
    ).migrate_records(
        records=[{"id": "a"}],
        source_schema=source,
        target_schema=target,
    )
    assert result == ({"id": "a", "state": "ok"},)
    assert lookup.lookups == [("steps", "1.1.0")]


def test_validation_catches_invalid_intermediate_record() -> None:
    source, middle, target = _step_schemas()
    migrations = MigrationRegistry(
        (
            MigrationStep("1.0.0", "1.1.0", (SetDefault("status", 404),)),
            MigrationStep("1.1.0", "2.0.0", (RenameField("status", "state"),)),
        )
    )
    with pytest.raises(SchemaEvolutionError, match=r"record\[0\].*status"):
        SchemaEvolutionService(
            migrations=migrations,
            intermediate_schemas=_IntermediateSchemas(middle),
        ).migrate_records(
            records=[{"id": "a"}],
            source_schema=source,
            target_schema=target,
        )


def test_intermediate_schema_must_match_requested_version() -> None:
    source, _middle, target = _step_schemas()
    migrations = MigrationRegistry(
        (
            MigrationStep("1.0.0", "1.1.0", ()),
            MigrationStep("1.1.0", "2.0.0", ()),
        )
    )
    with pytest.raises(SchemaEvolutionError, match="incorrect intermediate"):
        SchemaEvolutionService(
            migrations=migrations,
            intermediate_schemas=_IntermediateSchemas(target),
        ).migrate_records(
            records=[{"id": "a"}],
            source_schema=source,
            target_schema=target,
        )


class _BrokenResolver:
    def resolve(self, *, source_version: str, target_version: str):
        return ()


def test_injected_resolver_must_reach_target_version() -> None:
    source, _, target = _step_schemas()
    with pytest.raises(SchemaEvolutionError, match="reach target"):
        SchemaEvolutionService(
            migrations=_BrokenResolver()
        ).migrate_records(
            records=[], source_schema=source, target_schema=target
        )


class _PersistenceSpy:
    def __init__(self) -> None:
        self.calls = 0

    def commit_migration(self, **kwargs: object) -> MigrationAuditEvent:
        self.calls += 1
        return MigrationAuditEvent(
            event_id="audit-1",
            schema_name="test",
            operation="migration",
            source_version="1.0.0",
            target_version="1.1.0",
            source_hash="a",
            target_hash="b",
            record_count=1,
            occurred_at=datetime.now(UTC),
        )

    def rollback_last(self, *, schema_name: str) -> MigrationAuditEvent:
        raise NotImplementedError


class _TelemetrySpy:
    def __init__(self, *, fail: bool = False) -> None:
        self.calls = 0
        self.fail = fail

    def publish(self, event: MigrationAuditEvent) -> None:
        self.calls += 1
        if self.fail:
            raise OSError("telemetry unavailable")


def test_coordinator_does_not_commit_failed_migrations() -> None:
    persistence = _PersistenceSpy()
    coordinator = DatasetMigrationCoordinator(
        migrator=SchemaEvolutionService(
            migrations=MigrationRegistry(
                [MigrationStep("1.0.0", "1.1.0", ())]
            )
        ),
        persistence=persistence,
    )
    with pytest.raises(SchemaEvolutionError):
        coordinator.execute(
            records=[{"id": 123}],
            source_schema=DatasetRecordSchema(
                "test", "1.0.0", (DatasetField("id", "string"),)
            ),
            target_schema=DatasetRecordSchema(
                "test", "1.1.0", (DatasetField("id", "string"),)
            ),
        )
    assert persistence.calls == 0


def test_telemetry_failure_does_not_invalidate_committed_migration(
    caplog: pytest.LogCaptureFixture,
) -> None:
    persistence = _PersistenceSpy()
    telemetry = _TelemetrySpy(fail=True)
    coordinator = DatasetMigrationCoordinator(
        migrator=SchemaEvolutionService(
            migrations=MigrationRegistry(
                [MigrationStep("1.0.0", "1.1.0", ())]
            )
        ),
        persistence=persistence,
        telemetry=telemetry,
    )
    event = coordinator.execute(
        records=[{"id": "ok"}],
        source_schema=DatasetRecordSchema(
            "test", "1.0.0", (DatasetField("id", "string"),)
        ),
        target_schema=DatasetRecordSchema(
            "test", "1.1.0", (DatasetField("id", "string"),)
        ),
    )
    assert event.event_id == "audit-1"
    assert persistence.calls == 1
    assert telemetry.calls == 1
    assert "telemetry delivery failed" in caplog.text
