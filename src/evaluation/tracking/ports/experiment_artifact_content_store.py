from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from pathlib import Path

from src.evaluation.tracking.entities.experiment_artifact import (
    ExperimentArtifact,
)


class ExperimentArtifactContentStore(
    ABC,
):
    """
    Store port for artifact content persistence.
    """

    @abstractmethod
    def upload_file(
        self,
        *,
        local_path: Path,
        artifact: ExperimentArtifact,
    ) -> ExperimentArtifact:
        """
        Uploads artifact content.
        """