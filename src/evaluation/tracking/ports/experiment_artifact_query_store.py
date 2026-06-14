from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from src.evaluation.tracking.entities.experiment_artifact import (
    ExperimentArtifact,
)
from src.evaluation.tracking.enums.experiment_artifact_type import (
    ExperimentArtifactType,
)


class ExperimentArtifactQueryStore(
    ABC,
):
    """
    Store port for artifact querying.
    """

    @abstractmethod
    def get_by_id(
        self,
        *,
        artifact_id: str,
    ) -> ExperimentArtifact | None:
        """
        Returns artifact metadata by id.
        """

    @abstractmethod
    def list_by_run(
        self,
        *,
        run_id: str,
    ) -> tuple[
        ExperimentArtifact,
        ...,
    ]:
        """
        Lists artifacts by run.
        """

    @abstractmethod
    def list_by_experiment(
        self,
        *,
        experiment_id: str,
    ) -> tuple[
        ExperimentArtifact,
        ...,
    ]:
        """
        Lists artifacts by experiment.
        """

    @abstractmethod
    def list_by_type(
        self,
        *,
        artifact_type: (
            ExperimentArtifactType
        ),
    ) -> tuple[
        ExperimentArtifact,
        ...,
    ]:
        """
        Lists artifacts by type.
        """