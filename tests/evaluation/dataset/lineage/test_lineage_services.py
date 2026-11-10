"""Domain validation, SOLID contracts and bounded DAG traversal tests."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from src.evaluation.dataset.lineage import (
    DatasetLineageError,
    DatasetLineageExplorer,
    DatasetLineageNode,
    DatasetLineageRecorder,
    DatasetRevision,
    LineageLimitExceededError,
    LineageNotFoundError,
    LineageAuditEvent,
    LineageRegistration,
    LineageRelation,
    ParentLink,
)


def _revision(name: str, version: str = "1.0.0") -> DatasetRevision:
    return DatasetRevision(dataset_id=name, version=version)


def _node(name: str, version: str = "1.0.0") -> DatasetLineageNode:
    return DatasetLineageNode.from_artifact(
        revision=_revision(name, version),
        content=f"{name}:{version}".encode(),
        producer="unit-test",
        created_at=datetime(2026, 11, 10, tzinfo=UTC),
    )


class _WriterSpy:
    def __init__(self) -> None:
        self.calls: list[tuple[DatasetLineageNode, tuple[ParentLink, ...]]] = []

    def register(self, *, node: DatasetLineageNode, parents):
        self.calls.append((node, parents))
        return LineageRegistration(
            created=True,
            event=LineageAuditEvent(
                event_id="test-id",
                revision=node.revision,
                content_sha256=node.content_sha256,
                parent_count=len(parents),
                occurred_at=datetime.now(UTC),
            ),
        )


class _GraphReader:
    def __init__(self, graph: dict[DatasetRevision, tuple[DatasetRevision, ...]]):
        self.graph = graph

    def get_node(self, *, revision: DatasetRevision):
        if revision not in self.graph:
            return None
        return _node(revision.dataset_id, revision.version)

    def get_parents(self, *, revision: DatasetRevision):
        return tuple(
            ParentLink(parent=parent, relation=LineageRelation.DERIVED_FROM)
            for parent in self.graph[revision]
        )

    def get_children(self, *, revision: DatasetRevision):
        return tuple(
            key
            for key, parents in self.graph.items()
            if revision in parents
        )

    def get_events(self, *, revision: DatasetRevision):
        return ()


def test_recorder_depends_on_writer_protocol() -> None:
    writer = _WriterSpy()
    node = _node("dataset")
    result = DatasetLineageRecorder(writer=writer).register(node=node)
    assert result.created
    assert result.event.revision == node.revision
    assert writer.calls == [(node, ())]


@pytest.mark.parametrize("name", ["", " ", "x" * 129])
def test_revision_rejects_bad_identity(name: str) -> None:
    with pytest.raises(DatasetLineageError, match="dataset_id"):
        _revision(name)


@pytest.mark.parametrize("version", ["v1.0.0", "1.0", "1.0.0-pre"])
def test_revision_rejects_non_semver(version: str) -> None:
    with pytest.raises(ValueError):
        _revision("valid", version)


def test_node_requires_sha256_and_aware_datetime() -> None:
    with pytest.raises(DatasetLineageError, match="SHA-256"):
        DatasetLineageNode(
            revision=_revision("valid"),
            content_sha256="not-a-checksum",
            producer="worker",
            created_at=datetime.now(UTC),
        )
    with pytest.raises(DatasetLineageError, match="timezone-aware"):
        DatasetLineageNode(
            revision=_revision("valid"),
            content_sha256="a" * 64,
            producer="worker",
            created_at=datetime(2026, 11, 10),
        )


def test_node_factory_hashes_exact_bytes_and_does_not_keep_payload() -> None:
    node = _node("dataset")
    assert len(node.content_sha256) == 64
    assert not hasattr(node, "content")
    with pytest.raises(DatasetLineageError, match="bytes"):
        DatasetLineageNode.from_artifact(
            revision=_revision("dataset"),
            content="not bytes",  # type: ignore[arg-type]
            producer="worker",
            created_at=datetime.now(UTC),
        )


def test_recorder_rejects_duplicate_parents_and_self_references() -> None:
    recorder = DatasetLineageRecorder(writer=_WriterSpy())
    node = _node("dataset", "2.0.0")
    link = ParentLink(
        parent=_revision("dataset", "1.0.0"),
        relation=LineageRelation.DERIVED_FROM,
    )
    with pytest.raises(DatasetLineageError, match="duplicate parent"):
        recorder.register(node=node, parents=(link, link))
    with pytest.raises(DatasetLineageError, match="itself"):
        recorder.register(
            node=node,
            parents=(
                ParentLink(
                    parent=node.revision,
                    relation=LineageRelation.DERIVED_FROM,
                ),
            ),
        )


def test_recorder_rejects_reverse_or_same_dataset_version() -> None:
    recorder = DatasetLineageRecorder(writer=_WriterSpy())
    with pytest.raises(DatasetLineageError, match="greater version"):
        recorder.register(
            node=_node("dataset", "1.0.0"),
            parents=(
                ParentLink(
                    parent=_revision("dataset", "2.0.0"),
                    relation=LineageRelation.DERIVED_FROM,
                ),
            ),
        )


def test_explorer_handles_diamond_without_duplicate_ancestors() -> None:
    root = _revision("root")
    left = _revision("left")
    right = _revision("right")
    merged = _revision("merged")
    reader = _GraphReader({
        root: (),
        left: (root,),
        right: (root,),
        merged: (left, right),
    })
    explorer = DatasetLineageExplorer(reader=reader)
    assert explorer.ancestors(revision=merged) == (left, right, root)
    assert explorer.descendants(revision=root) == (left, right, merged)


def test_explorer_rejects_unknown_revision_and_bounded_results() -> None:
    root = _revision("root")
    middle = _revision("middle")
    leaf = _revision("leaf")
    explorer = DatasetLineageExplorer(reader=_GraphReader({
        root: (),
        middle: (root,),
        leaf: (middle,),
    }))
    with pytest.raises(LineageNotFoundError, match="does not exist"):
        explorer.ancestors(revision=_revision("missing"))
    with pytest.raises(LineageLimitExceededError, match="max_depth"):
        explorer.ancestors(revision=leaf, max_depth=1)
    with pytest.raises(LineageLimitExceededError, match="max_nodes"):
        explorer.ancestors(revision=leaf, max_nodes=1)


@pytest.mark.parametrize("depth,nodes", [(-1, 1), (1, 0), (True, 1), (1, True)])
def test_explorer_rejects_invalid_bounds(depth: object, nodes: object) -> None:
    revision = _revision("root")
    explorer = DatasetLineageExplorer(
        reader=_GraphReader({revision: ()})
    )
    with pytest.raises(DatasetLineageError):
        explorer.ancestors(
            revision=revision,
            max_depth=depth,  # type: ignore[arg-type]
            max_nodes=nodes,  # type: ignore[arg-type]
        )


def test_explorer_defensively_handles_corrupt_cycle() -> None:
    a = _revision("a")
    b = _revision("b")
    explorer = DatasetLineageExplorer(
        reader=_GraphReader({a: (b,), b: (a,)})
    )
    assert explorer.ancestors(revision=a) == (b,)
