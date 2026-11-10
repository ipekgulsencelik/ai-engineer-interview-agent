"""Small repository protocols, independent of persistence technology."""

from __future__ import annotations

from typing import Protocol

from src.evaluation.dataset.lineage.models import (
    DatasetLineageNode,
    DatasetRevision,
    LineageAuditEvent,
    LineageRegistration,
    ParentLink,
)


class LineageWriter(Protocol):
    """Atomically register an immutable node and its parent relations."""

    def register(
        self,
        *,
        node: DatasetLineageNode,
        parents: tuple[ParentLink, ...],
    ) -> LineageRegistration: ...


class LineageReader(Protocol):
    """Bounded graph exploration of stored revisions."""

    def get_node(self, *, revision: DatasetRevision) -> DatasetLineageNode | None: ...

    def get_parents(self, *, revision: DatasetRevision) -> tuple[ParentLink, ...]: ...

    def get_children(
        self, *, revision: DatasetRevision
    ) -> tuple[DatasetRevision, ...]: ...

    def get_events(
        self, *, revision: DatasetRevision
    ) -> tuple[LineageAuditEvent, ...]: ...


class DatasetLineageRepository(LineageReader, LineageWriter, Protocol):
    """Complete repository contract; application services use smaller ports."""
