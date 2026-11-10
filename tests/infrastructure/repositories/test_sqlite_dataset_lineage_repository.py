"""SQLite lineage: atomicity, immutable provenance, impact and replay."""

from __future__ import annotations

import sqlite3
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime

import pytest

from src.evaluation.dataset.lineage import (
    DatasetLineageNode,
    DatasetLineageRecorder,
    DatasetLineageExplorer,
    DatasetRevision,
    LineageConflictError,
    LineageNotFoundError,
    LineageRelation,
    LineageStorageError,
    ParentLink,
)
from src.infrastructure.repositories.sqlite_dataset_lineage_repository import (
    SQLiteDatasetLineageRepository,
)


def _node(
    name: str,
    version: str = "1.0.0",
    *,
    payload: bytes | None = None,
) -> DatasetLineageNode:
    return DatasetLineageNode.from_artifact(
        revision=DatasetRevision(dataset_id=name, version=version),
        content=(
            payload if payload is not None
            else f"artifact:{name}:{version}".encode("utf-8")
        ),
        producer="dataset-builder",
        created_at=datetime(2026, 11, 10, 12, tzinfo=UTC),
        schema_version="1.0.0",
    )


def _link(
    node: DatasetLineageNode,
    relation: LineageRelation = LineageRelation.DERIVED_FROM,
) -> ParentLink:
    return ParentLink(parent=node.revision, relation=relation)


def test_root_and_derived_nodes_persist_after_reopen(tmp_path) -> None:
    path = tmp_path / "lineage.sqlite"
    store = SQLiteDatasetLineageRepository(path)
    recorder = DatasetLineageRecorder(writer=store)
    root = _node("training")
    derived = _node("training", "1.1.0")

    assert recorder.register(node=root).created
    event = recorder.register(
        node=derived, parents=(_link(root),)
    ).event

    reopened = SQLiteDatasetLineageRepository(path)
    assert reopened.get_node(revision=root.revision) == root
    assert reopened.get_node(revision=derived.revision) == derived
    assert reopened.get_parents(revision=derived.revision) == (_link(root),)
    assert reopened.get_children(revision=root.revision) == (derived.revision,)
    assert reopened.get_events(revision=derived.revision) == (event,)
    assert event.parent_count == 1


def test_multi_parent_provenance_and_downstream_impact(tmp_path) -> None:
    store = SQLiteDatasetLineageRepository(tmp_path / "lineage.sqlite")
    recorder = DatasetLineageRecorder(writer=store)
    a, b = _node("dataset-a"), _node("dataset-b")
    merger = _node("combined")
    product = _node("served")
    for node in (a, b):
        recorder.register(node=node)
    recorder.register(
        node=merger,
        parents=(
            _link(a, LineageRelation.MERGED_FROM),
            _link(b, LineageRelation.MERGED_FROM),
        ),
    )
    recorder.register(
        node=product,
        parents=(_link(merger, LineageRelation.FILTERED_FROM),),
    )

    explorer = DatasetLineageExplorer(reader=store)
    assert explorer.ancestors(revision=product.revision) == (
        merger.revision, a.revision, b.revision,
    )
    assert explorer.descendants(revision=a.revision) == (
        merger.revision, product.revision,
    )


def test_idempotent_retry_does_not_duplicate_events(tmp_path) -> None:
    path = tmp_path / "lineage.sqlite"
    store = SQLiteDatasetLineageRepository(path)
    node = _node("dataset")
    first = store.register(node=node, parents=())
    second = SQLiteDatasetLineageRepository(path).register(
        node=node, parents=()
    )

    assert first.created
    assert not second.created
    assert first.event.event_id == second.event.event_id
    assert len(store.get_events(revision=node.revision)) == 1


def test_retry_is_independent_of_parent_link_order(tmp_path) -> None:
    store = SQLiteDatasetLineageRepository(tmp_path / "lineage.sqlite")
    parent_a, parent_b = _node("a"), _node("b")
    child = _node("merged")
    for parent in (parent_a, parent_b):
        store.register(node=parent, parents=())
    links = (
        _link(parent_a, LineageRelation.MERGED_FROM),
        _link(parent_b, LineageRelation.MERGED_FROM),
    )
    first = store.register(node=child, parents=links)
    second = store.register(node=child, parents=links[::-1])
    assert first.created
    assert not second.created
    assert first.event == second.event


def test_conflicting_same_version_is_rejected_without_update(tmp_path) -> None:
    store = SQLiteDatasetLineageRepository(tmp_path / "lineage.sqlite")
    original = _node("training", payload=b"original")
    store.register(node=original, parents=())
    with pytest.raises(LineageConflictError, match="different provenance"):
        store.register(
            node=_node("training", payload=b"rewritten"),
            parents=(),
        )
    assert store.get_node(revision=original.revision) == original


def test_existing_revision_cannot_change_its_parent_set(tmp_path) -> None:
    store = SQLiteDatasetLineageRepository(tmp_path / "lineage.sqlite")
    root = _node("root")
    child = _node("child")
    store.register(node=root, parents=())
    store.register(node=child, parents=())
    with pytest.raises(LineageConflictError, match="different provenance"):
        store.register(node=child, parents=(_link(root),))
    assert store.get_parents(revision=child.revision) == ()


def test_missing_parent_is_rejected_atomically(tmp_path) -> None:
    store = SQLiteDatasetLineageRepository(tmp_path / "lineage.sqlite")
    child = _node("child")
    missing = _node("missing")
    with pytest.raises(LineageNotFoundError, match="parent"):
        store.register(node=child, parents=(_link(missing),))
    assert store.get_node(revision=child.revision) is None


def test_duplicate_parent_relation_is_rejected_before_writes(tmp_path) -> None:
    store = SQLiteDatasetLineageRepository(tmp_path / "lineage.sqlite")
    root, child = _node("root"), _node("child")
    store.register(node=root, parents=())
    with pytest.raises(ValueError, match="duplicate parent"):
        store.register(
            node=child,
            parents=(
                _link(root, LineageRelation.MERGED_FROM),
                _link(root, LineageRelation.DERIVED_FROM),
            ),
        )
    assert store.get_node(revision=child.revision) is None


def test_database_trigger_failure_rolls_back_node_and_edges(tmp_path) -> None:
    path = tmp_path / "lineage.sqlite"
    store = SQLiteDatasetLineageRepository(path)
    root, child = _node("root"), _node("child")
    store.register(node=root, parents=())
    with sqlite3.connect(path) as conn:
        conn.execute(
            """
            CREATE TRIGGER abort_lineage_audit
            BEFORE INSERT ON dataset_lineage_audit
            BEGIN SELECT RAISE(ABORT, 'injected failure'); END
            """
        )
    with pytest.raises(LineageStorageError, match="transaction failed"):
        store.register(node=child, parents=(_link(root),))
    assert store.get_node(revision=child.revision) is None
    assert store.get_children(revision=root.revision) == ()
    assert len(store.get_events(revision=root.revision)) == 1
    with sqlite3.connect(path) as conn:
        count = conn.execute(
            "SELECT COUNT(*) FROM dataset_lineage_edges"
        ).fetchone()[0]
    assert count == 0


def test_concurrent_retry_creates_one_event_and_one_revision(tmp_path) -> None:
    path = tmp_path / "lineage.sqlite"
    SQLiteDatasetLineageRepository(path)
    node = _node("parallel")

    def attempt(_index: int):
        return SQLiteDatasetLineageRepository(path).register(
            node=node, parents=()
        )

    with ThreadPoolExecutor(max_workers=6) as pool:
        attempts = list(pool.map(attempt, range(6)))

    assert sum(result.created for result in attempts) == 1
    assert len({result.event.event_id for result in attempts}) == 1


def test_storage_contains_no_raw_artifact_content(tmp_path) -> None:
    path = tmp_path / "lineage.sqlite"
    store = SQLiteDatasetLineageRepository(path)
    payload = b"DO-NOT-PERSIST-SENSITIVE-SAMPLE-CONTENT-93bf7"
    node = _node("sensitive", payload=payload)
    store.register(node=node, parents=())
    assert payload not in path.read_bytes()
    assert node.content_sha256 == store.get_events(
        revision=node.revision
    )[0].content_sha256


def test_unknown_revision_query_is_explicit(tmp_path) -> None:
    store = SQLiteDatasetLineageRepository(tmp_path / "lineage.sqlite")
    revision = DatasetRevision(dataset_id="missing", version="1.0.0")
    assert store.get_node(revision=revision) is None
    with pytest.raises(LineageNotFoundError):
        store.get_parents(revision=revision)
    with pytest.raises(LineageNotFoundError):
        store.get_children(revision=revision)
    with pytest.raises(LineageNotFoundError):
        store.get_events(revision=revision)


def test_storage_rejects_ephemeral_in_memory_database() -> None:
    with pytest.raises(ValueError, match="file-backed"):
        SQLiteDatasetLineageRepository(":memory:")
