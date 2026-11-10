"""Dataset lineage application services with dependency-inverted storage."""

from __future__ import annotations

from collections import deque

from src.evaluation.dataset.lineage.errors import (
    DatasetLineageError,
    LineageLimitExceededError,
    LineageNotFoundError,
)
from src.evaluation.dataset.lineage.models import (
    DatasetLineageNode,
    DatasetRevision,
    LineageRegistration,
    ParentLink,
)
from src.evaluation.dataset.lineage.ports import LineageReader, LineageWriter
from src.evaluation.dataset.schema_evolution.models import parse_schema_version


def validate_registration(
    *,
    node: DatasetLineageNode,
    parents: tuple[ParentLink, ...],
) -> None:
    """Enforce DAG-safe, bounded, unambiguous parent declarations."""
    if not isinstance(node, DatasetLineageNode):
        raise DatasetLineageError("node must be a DatasetLineageNode")
    if not isinstance(parents, tuple):
        raise DatasetLineageError("parents must be a tuple")
    if len(parents) > 256:
        raise DatasetLineageError("a revision cannot have over 256 parents")
    seen: set[DatasetRevision] = set()
    for link in parents:
        if not isinstance(link, ParentLink):
            raise DatasetLineageError("parents must contain ParentLink objects")
        if link.parent == node.revision:
            raise DatasetLineageError("a dataset cannot depend on itself")
        if link.parent in seen:
            raise DatasetLineageError("duplicate parent revision")
        seen.add(link.parent)
        if (
            link.parent.dataset_id == node.revision.dataset_id
            and parse_schema_version(link.parent.version)
            >= parse_schema_version(node.revision.version)
        ):
            raise DatasetLineageError(
                "the same dataset must evolve to a greater version"
            )


class DatasetLineageRecorder:
    """Register derived datasets without coupling to SQL or a graph database."""

    def __init__(self, *, writer: LineageWriter) -> None:
        self._writer = writer

    def register(
        self,
        *,
        node: DatasetLineageNode,
        parents: tuple[ParentLink, ...] = (),
    ) -> LineageRegistration:
        validate_registration(node=node, parents=parents)
        return self._writer.register(node=node, parents=parents)


class DatasetLineageExplorer:
    """Explore immutable upstream provenance and downstream impact."""

    def __init__(self, *, reader: LineageReader) -> None:
        self._reader = reader

    def ancestors(
        self,
        *,
        revision: DatasetRevision,
        max_depth: int = 32,
        max_nodes: int = 1000,
    ) -> tuple[DatasetRevision, ...]:
        return self._walk(
            revision=revision,
            upstream=True,
            max_depth=max_depth,
            max_nodes=max_nodes,
        )

    def descendants(
        self,
        *,
        revision: DatasetRevision,
        max_depth: int = 32,
        max_nodes: int = 1000,
    ) -> tuple[DatasetRevision, ...]:
        return self._walk(
            revision=revision,
            upstream=False,
            max_depth=max_depth,
            max_nodes=max_nodes,
        )

    def _walk(
        self,
        *,
        revision: DatasetRevision,
        upstream: bool,
        max_depth: int,
        max_nodes: int,
    ) -> tuple[DatasetRevision, ...]:
        if type(max_depth) is not int or max_depth < 0:
            raise DatasetLineageError("max_depth must be a nonnegative integer")
        if type(max_nodes) is not int or max_nodes < 1:
            raise DatasetLineageError("max_nodes must be a positive integer")
        if self._reader.get_node(revision=revision) is None:
            raise LineageNotFoundError("dataset revision does not exist")

        queue = deque([(revision, 0)])
        seen = {revision}
        ordered: list[DatasetRevision] = []
        while queue:
            current, depth = queue.popleft()
            if upstream:
                neighbors = tuple(
                    link.parent
                    for link in self._reader.get_parents(revision=current)
                )
            else:
                neighbors = self._reader.get_children(revision=current)
            for neighbor in sorted(neighbors):
                if neighbor in seen:
                    continue
                if depth >= max_depth:
                    raise LineageLimitExceededError(
                        "lineage exceeds max_depth; result would be incomplete"
                    )
                if len(ordered) >= max_nodes:
                    raise LineageLimitExceededError(
                        "lineage exceeds max_nodes; result would be incomplete"
                    )
                if self._reader.get_node(revision=neighbor) is None:
                    raise LineageNotFoundError(
                        "lineage contains a missing related revision"
                    )
                seen.add(neighbor)
                ordered.append(neighbor)
                queue.append((neighbor, depth + 1))
        return tuple(ordered)
