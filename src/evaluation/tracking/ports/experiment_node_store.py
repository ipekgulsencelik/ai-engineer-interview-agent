from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from src.evaluation.tracking.entities.experiment_node import (
    ExperimentNode,
)


class ExperimentNodeStore(
    ABC,
):
    """
    Store port for experiment lineage node persistence.
    """

    @abstractmethod
    def save_node(
        self,
        *,
        node: ExperimentNode,
    ) -> None:
        """
        Persists an experiment lineage node.
        """

    @abstractmethod
    def get_node(
        self,
        *,
        experiment_id: str,
    ) -> ExperimentNode | None:
        """
        Returns a lineage node by experiment id.
        """

    @abstractmethod
    def list_nodes(
        self,
    ) -> tuple[
        ExperimentNode,
        ...,
    ]:
        """
        Lists all lineage nodes.
        """

    @abstractmethod
    def exists_node(
        self,
        *,
        experiment_id: str,
    ) -> bool:
        """
        Returns whether a node exists.
        """