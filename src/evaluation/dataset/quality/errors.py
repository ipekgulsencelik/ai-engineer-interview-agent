"""Domain exceptions for advanced dataset quality validation."""


class DatasetQualityError(ValueError):
    """Invalid quality configuration, report or dataset input."""


class QualityRuleExecutionError(DatasetQualityError):
    """A validation rule failed unexpectedly: validation fails closed."""


class QualityReportStorageError(DatasetQualityError):
    """Durable quality report storage failed or was corrupted."""
