"""Domain-level errors for dataset provenance and lineage."""


class DatasetLineageError(ValueError):
    """Base exception for invalid or unavailable dataset lineage."""


class LineageConflictError(DatasetLineageError):
    """An immutable revision was already recorded with different provenance."""


class LineageNotFoundError(DatasetLineageError):
    """The requested dataset revision or parent does not exist."""


class LineageLimitExceededError(DatasetLineageError):
    """Traversal would exceed its explicit safety limits."""


class LineageStorageError(DatasetLineageError):
    """The durable lineage repository could not complete an operation."""
