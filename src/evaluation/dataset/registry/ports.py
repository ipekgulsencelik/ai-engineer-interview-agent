"""Dependency-inverted, deliberately narrow registry storage contracts."""

from __future__ import annotations

from typing import Protocol

from src.evaluation.dataset.lineage.models import (
    DatasetLineageNode,
    DatasetRevision,
)
from src.evaluation.dataset.registry.models import DatasetCatalogEntry


class DatasetLineageLookup(Protocol):
    def get_node(self, *, revision: DatasetRevision) -> DatasetLineageNode | None: ...


class RegistryWriter(Protocol):
    def register(self, *, entry: DatasetCatalogEntry) -> bool: ...


class RegistryReader(Protocol):
    def get(self, *, revision: DatasetRevision) -> DatasetCatalogEntry | None: ...

    def list_versions(
        self, *, dataset_id: str, limit: int = 100
    ) -> tuple[DatasetCatalogEntry, ...]: ...

    def list_by_tag(
        self, *, tag: str, limit: int = 100
    ) -> tuple[DatasetCatalogEntry, ...]: ...


class RegistryStore(RegistryReader, RegistryWriter, Protocol):
    """Combined port for the catalog use case; no SQL dependency."""
