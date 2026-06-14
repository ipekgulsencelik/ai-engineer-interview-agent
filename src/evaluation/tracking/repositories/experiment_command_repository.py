from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from src.evaluation.tracking.entities.experiment_node import (
    ExperimentNode,
)


class ExperimentCommandRepository(
    ABC,
):
    """
    Repository port for experiment write operations.
    """

    @abstractmethod
    def save(
        self,
        *,
        experiment: ExperimentNode,
    ) -> None:
        """
        Persists a new experiment.
        """

    @abstractmethod
    def update(
        self,
        *,
        experiment: ExperimentNode,
    ) -> None:
        """
        Updates an existing experiment.
        """

    @abstractmethod
    def delete(
        self,
        *,
        experiment_id: str,
    ) -> None:
        """
        Deletes experiment metadata.
        """