"""Registry-specific, value-redacting domain and storage errors."""


class DatasetRegistryError(ValueError):
    """A registry contract could not be satisfied."""


class DatasetRegistryConflictError(DatasetRegistryError):
    """Immutable revision identity or monotonic version policy conflicts."""


class DatasetRegistryLineageError(DatasetRegistryError):
    """The proposed revision is not backed by matching persisted lineage."""


class DatasetRegistryStorageError(DatasetRegistryError):
    """A durable registry operation failed or persisted data was corrupted."""
