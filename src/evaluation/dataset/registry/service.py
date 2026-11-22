"""Application use case for registering lineage-backed dataset revisions."""

from __future__ import annotations

from src.evaluation.dataset.lineage.models import (
    DatasetLineageNode,
    DatasetRevision,
)
from src.evaluation.dataset.registry.errors import DatasetRegistryLineageError
from src.evaluation.dataset.registry.models import (
    CatalogRegistration,
    DatasetCatalogEntry,
)
from src.evaluation.dataset.registry.ports import (
    DatasetLineageLookup,
    RegistryStore,
)


class DatasetRegistryService:
    """Register only provenance-backed metadata; never persist raw samples."""

    def __init__(
        self, *, lineage: DatasetLineageLookup, registry: RegistryStore
    ) -> None:
        self._lineage = lineage
        self._registry = registry

    def register(
        self,
        *,
        node: DatasetLineageNode,
        name: str,
        owner_id: str,
        tags: tuple[str, ...] = (),
        description: str | None = None,
    ) -> CatalogRegistration:
        entry = DatasetCatalogEntry.from_lineage(
            node=node,
            name=name,
            owner_id=owner_id,
            tags=tags,
            description=description,
        )
        stored = self._lineage.get_node(revision=node.revision)
        if stored != node:
            raise DatasetRegistryLineageError(
                "matching immutable lineage revision must be registered first"
            )
        return CatalogRegistration(
            created=self._registry.register(entry=entry), entry=entry
        )

    def get(self, *, revision: DatasetRevision) -> DatasetCatalogEntry | None:
        return self._registry.get(revision=revision)

    def list_versions(
        self, *, dataset_id: str, limit: int = 100
    ) -> tuple[DatasetCatalogEntry, ...]:
        return self._registry.list_versions(dataset_id=dataset_id, limit=limit)

    def list_by_tag(
        self, *, tag: str, limit: int = 100
    ) -> tuple[DatasetCatalogEntry, ...]:
        return self._registry.list_by_tag(tag=tag, limit=limit)
