"""Errors raised by dataset monitoring and alert dispatch."""


class DatasetObservabilityError(ValueError):
    """Invalid or inconsistent monitoring inputs."""


class ObservabilityStorageError(DatasetObservabilityError):
    """Monitoring state persistence or integrity verification failed."""


class AlertDeliveryError(RuntimeError):
    """An alert could not be delivered or acknowledged."""
