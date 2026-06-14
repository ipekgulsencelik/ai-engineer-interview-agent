from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from src.evaluation.tracking.entities.experiment_node import (
    ExperimentNode,
)


class ExperimentQueryRepository(
    ABC,
):
    """
    Repository port for experiment lookups.
    """

    @abstractmethod
    def get_by_id(
        self,
        *,
        experiment_id: str,
    ) -> ExperimentNode | None:
        """
        Returns experiment by id.
        """

    @abstractmethod
    def list_all(
        self,
    ) -> tuple[
        ExperimentNode,
        ...,
    ]:
        """
        Lists all experiments.
        """

    @abstractmethod
    def list_by_name(
        self,
        *,
        experiment_name: str,
    ) -> tuple[
        ExperimentNode,
        ...,
    ]:
        """
        Lists experiments by name.
        """

    @abstractmethod
    def list_by_version(
        self,
        *,
        experiment_version: str,
    ) -> tuple[
        ExperimentNode,
        ...,
    ]:
        """
        Lists experiments by version.
        """

    @abstractmethod
    def exists(
        self,
        *,
        experiment_id: str,
    ) -> bool:
        """
        Returns whether experiment exists.
        """