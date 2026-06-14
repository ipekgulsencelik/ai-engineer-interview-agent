from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from src.evaluation.tracking.entities.experiment_artifact import (
    ExperimentArtifact,
)


class ExperimentArtifactMetadataStore(
    ABC,
):
    """
    Store port for artifact metadata persistence.
    """

    @abstractmethod
    def save(
        self,
        *,
        artifact: ExperimentArtifact,
    ) -> None:
        """
        Persists artifact metadata.
        """

    @abstractmethod
    def delete(
        self,
        *,
        artifact_id: str,
    ) -> None:
        """
        Deletes artifact metadata.
        """

    @abstractmethod
    def exists(
        self,
        *,
        artifact_id: str,
    ) -> bool:
        """
        Returns whether artifact metadata exists.
        """