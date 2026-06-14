from __future__ import annotations

from src.evaluation.tracking.clients.external_artifact_tracking_client import (
    ExternalArtifactTrackingClient,
)
from src.evaluation.tracking.clients.external_client_lifecycle import (
    ExternalClientLifecycle,
)
from src.evaluation.tracking.clients.external_event_tracking_client import (
    ExternalEventTrackingClient,
)
from src.evaluation.tracking.clients.external_model_registry_client import (
    ExternalModelRegistryClient,
)
from src.evaluation.tracking.clients.external_run_tracking_client import (
    ExternalRunTrackingClient,
)


class ExternalTrackingClient(
    ExternalEventTrackingClient,
    ExternalRunTrackingClient,
    ExternalArtifactTrackingClient,
    ExternalModelRegistryClient,
    ExternalClientLifecycle,
):
    """
    Composite client port for complete external tracking integrations.
    """

    # This class intentionally left blank as a composite of all external tracking client interfaces.
    pass