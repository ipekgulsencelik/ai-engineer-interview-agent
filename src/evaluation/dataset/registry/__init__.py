"""Immutable, lineage-backed dataset registry and version catalog."""

from src.evaluation.dataset.registry.errors import (
    DatasetRegistryConflictError,
    DatasetRegistryError,
    DatasetRegistryLineageError,
    DatasetRegistryStorageError,
)
from src.evaluation.dataset.registry.models import (
    CatalogRegistration,
    DatasetCatalogEntry,
)
from src.evaluation.dataset.registry.ports import (
    DatasetLineageLookup,
    RegistryReader,
    RegistryStore,
    RegistryWriter,
)
from src.evaluation.dataset.registry.service import DatasetRegistryService

__all__ = [
    "CatalogRegistration",
    "DatasetCatalogEntry",
    "DatasetLineageLookup",
    "DatasetRegistryConflictError",
    "DatasetRegistryError",
    "DatasetRegistryLineageError",
    "DatasetRegistryService",
    "DatasetRegistryStorageError",
    "RegistryReader",
    "RegistryStore",
    "RegistryWriter",
]
