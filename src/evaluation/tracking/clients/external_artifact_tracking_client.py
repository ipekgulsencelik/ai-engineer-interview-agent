from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from src.evaluation.tracking.entities.experiment_artifact import (
    ExperimentArtifact,
)


class ExternalArtifactTrackingClient(
    ABC,
):
    """
    Client port for external artifact tracking.
    """

    @abstractmethod
    async def log_artifact(
        self,
        *,
        artifact: ExperimentArtifact,
    ) -> None:
        """
        Sends artifact metadata to the external system.
        """

    @abstractmethod
    async def upload_artifact(
        self,
        *,
        artifact: ExperimentArtifact,
    ) -> None:
        """
        Uploads or registers an artifact in the external system.
        """