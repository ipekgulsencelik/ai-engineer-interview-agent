"""SQLite registry: version ordering, concurrent writes, audit and corruption."""

from __future__ import annotations

import sqlite3
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from datetime import UTC, datetime

import pytest

from src.evaluation.dataset.lineage.models import (
    DatasetLineageNode,
    DatasetRevision,
)
from src.evaluation.dataset.registry import (
    DatasetCatalogEntry,
    DatasetRegistryConflictError,
    DatasetRegistryError,
    DatasetRegistryStorageError,
)
from src.infrastructure.repositories.sqlite_dataset_registry_repository import (
    SQLiteDatasetRegistryRepository,
)


def _entry(
    version: str,
    *,
    dataset_id: str = "evaluation",
    tags: tuple[str, ...] = ("training",),
) -> DatasetCatalogEntry:
    node = DatasetLineageNode.from_artifact(
        revision=DatasetRevision(dataset_id=dataset_id, version=version),
        content=f"{dataset_id}:{version}".encode(),
        created_at=datetime(2026, 11, 23, tzinfo=UTC),
        producer="test-producer",
    )
    return DatasetCatalogEntry.from_lineage(
        node=node, name="Evaluation Dataset", owner_id="quality-team", tags=tags
    )


def test_versions_use_numeric_semver_order_and_cannot_move_backwards(tmp_path) -> None:
    repo = SQLiteDatasetRegistryRepository(tmp_path / "registry.sqlite")
    versions = ("1.2.0", "1.10.0", "2.0.0")
    for version in versions:
        assert repo.register(entry=_entry(version))

    assert tuple(
        entry.revision.version for entry in repo.list_versions(dataset_id="evaluation")
    ) == tuple(reversed(versions))
    assert repo.list_versions(dataset_id="evaluation", limit=1)[0].revision.version == (
        "2.0.0"
    )
    with pytest.raises(DatasetRegistryConflictError, match="greater"):
        repo.register(entry=_entry("1.99.0"))
    with pytest.raises(DatasetRegistryConflictError, match="greater"):
        repo.register(entry=_entry("0.99.99"))
    assert repo.get(
        revision=DatasetRevision(dataset_id="evaluation", version="1.99.0")
    ) is None


def test_idempotency_conflict_and_atomic_audit(tmp_path) -> None:
    path = tmp_path / "registry.sqlite"
    repo = SQLiteDatasetRegistryRepository(path)
    first = _entry("1.0.0", tags=("curated", "training"))
    assert repo.register(entry=first)
    assert not repo.register(entry=first)
    with pytest.raises(DatasetRegistryConflictError, match="different metadata"):
        repo.register(entry=replace(first, owner_id="different-team"))
    with sqlite3.connect(path) as conn:
        count = conn.execute("SELECT COUNT(*) FROM dataset_registry_entries").fetchone()
        assert count == (1,)
        count = conn.execute("SELECT COUNT(*) FROM dataset_registry_tags").fetchone()
        assert count == (2,)
        count = conn.execute("SELECT COUNT(*) FROM dataset_registry_audit").fetchone()
        assert count == (1,)


def test_tag_queries_are_bounded_and_deterministic(tmp_path) -> None:
    repo = SQLiteDatasetRegistryRepository(tmp_path / "registry.sqlite")
    entries = (
        _entry("1.0.0", dataset_id="alpha", tags=("public",)),
        _entry("1.1.0", dataset_id="alpha", tags=("curated", "public")),
        _entry("1.0.0", dataset_id="beta", tags=("public",)),
    )
    for entry in entries:
        repo.register(entry=entry)
    assert tuple(
        (entry.revision.dataset_id, entry.revision.version)
        for entry in repo.list_by_tag(tag="public")
    ) == (("alpha", "1.1.0"), ("alpha", "1.0.0"), ("beta", "1.0.0"))
    assert len(repo.list_by_tag(tag="public", limit=2)) == 2
    assert repo.list_by_tag(tag="unknown") == ()
    assert repo.list_versions(dataset_id="not-registered") == ()


@pytest.mark.parametrize("limit", [0, -1, 1001, True, 1.5])
def test_bad_query_limits_are_rejected(tmp_path, limit: object) -> None:
    repo = SQLiteDatasetRegistryRepository(tmp_path / "registry.sqlite")
    with pytest.raises(DatasetRegistryError, match="limit"):
        repo.list_versions(  # type: ignore[arg-type]
            dataset_id="evaluation", limit=limit
        )
    with pytest.raises(DatasetRegistryError, match="limit"):
        repo.list_by_tag(tag="training", limit=limit)  # type: ignore[arg-type]


@pytest.mark.parametrize("tag", ["UPPER", "bad tag", "", "a" * 65])
def test_bad_query_tags_are_rejected(tmp_path, tag: str) -> None:
    repo = SQLiteDatasetRegistryRepository(tmp_path / "registry.sqlite")
    with pytest.raises(DatasetRegistryError, match="tag"):
        repo.list_by_tag(tag=tag)


def test_checksum_tampering_and_tag_projection_tampering_fail_closed(
    tmp_path,
) -> None:
    path = tmp_path / "registry.sqlite"
    repo = SQLiteDatasetRegistryRepository(path)
    entry = _entry("1.0.0")
    repo.register(entry=entry)
    with sqlite3.connect(path) as conn:
        conn.execute(
            "UPDATE dataset_registry_entries SET entry_json = ?",
            ('{"forged":true}',),
        )
    with pytest.raises(DatasetRegistryStorageError, match="checksum"):
        repo.get(revision=entry.revision)
    with sqlite3.connect(path) as conn:
        conn.execute(
            "UPDATE dataset_registry_entries SET entry_json = ?",
            ('{"forged":true}',),
        )
        # Restore via exact canonical JSON from a new database-independent entry.
        from src.infrastructure.repositories.sqlite_dataset_registry_repository import (
            _checksum,
            _serialize,
        )

        content = _serialize(entry)
        conn.execute(
            "UPDATE dataset_registry_entries SET entry_json = ?, checksum = ?",
            (content, _checksum(content)),
        )
        conn.execute("DELETE FROM dataset_registry_tags")
    with pytest.raises(DatasetRegistryStorageError, match="invalid"):
        repo.get(revision=entry.revision)


def test_audit_failure_rolls_back_entry_and_tag_projection(tmp_path) -> None:
    path = tmp_path / "registry.sqlite"
    repo = SQLiteDatasetRegistryRepository(path)
    with sqlite3.connect(path) as conn:
        conn.execute(
            """
            CREATE TRIGGER fail_catalog_audit
            BEFORE INSERT ON dataset_registry_audit
            BEGIN
                SELECT RAISE(ABORT, 'injected-audit-failure');
            END;
            """
        )
    entry = _entry("1.0.0")
    with pytest.raises(DatasetRegistryStorageError, match="transaction"):
        repo.register(entry=entry)
    assert repo.get(revision=entry.revision) is None
    with sqlite3.connect(path) as conn:
        count = conn.execute("SELECT COUNT(*) FROM dataset_registry_entries").fetchone()
        assert count == (0,)
        count = conn.execute("SELECT COUNT(*) FROM dataset_registry_tags").fetchone()
        assert count == (0,)


def test_simultaneous_exact_registration_creates_one_row_and_audit(
    tmp_path,
) -> None:
    path = tmp_path / "registry.sqlite"
    repo = SQLiteDatasetRegistryRepository(path)
    entry = _entry("1.0.0")
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = [pool.submit(repo.register, entry=entry) for _ in range(8)]
        results = [future.result() for future in futures]
    assert results.count(True) == 1
    assert results.count(False) == 7
    with sqlite3.connect(path) as conn:
        count = conn.execute("SELECT COUNT(*) FROM dataset_registry_audit").fetchone()
        assert count == (1,)


def test_non_file_sqlite_and_bad_timeout_are_rejected(tmp_path) -> None:
    with pytest.raises(DatasetRegistryError, match="file-backed"):
        SQLiteDatasetRegistryRepository(":memory:")
    for timeout in (0, -1, True, float("nan")):
        with pytest.raises(DatasetRegistryError, match="timeout"):
            SQLiteDatasetRegistryRepository(
                tmp_path / "registry.sqlite", timeout=timeout
            )


def test_version_index_corruption_is_not_silently_trusted(tmp_path) -> None:
    path = tmp_path / "registry.sqlite"
    repo = SQLiteDatasetRegistryRepository(path)
    entry = _entry("1.5.0")
    repo.register(entry=entry)
    with sqlite3.connect(path) as conn:
        conn.execute(
            "UPDATE dataset_registry_entries SET version_minor = 999 "
            "WHERE dataset_id = ?",
            (entry.revision.dataset_id,),
        )
    with pytest.raises(DatasetRegistryStorageError, match="invalid"):
        repo.get(revision=entry.revision)
    with pytest.raises(DatasetRegistryStorageError, match="invalid"):
        repo.list_versions(dataset_id=entry.revision.dataset_id)
