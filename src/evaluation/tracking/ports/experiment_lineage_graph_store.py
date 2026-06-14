from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from src.evaluation.tracking.entities.experiment_lineage_graph import (
    ExperimentLineageGraph,
)


class ExperimentLineageGraphStore(
    ABC,
):
    """
    Store port for experiment lineage graph persistence.
    """

    @abstractmethod
    def save_graph(
        self,
        *,
        graph: ExperimentLineageGraph,
    ) -> None:
        """
        Persists an experiment lineage graph.
        """

    @abstractmethod
    def get_graph(
        self,
        *,
        graph_id: str,
    ) -> ExperimentLineageGraph | None:
        """
        Returns a lineage graph by id.
        """

    @abstractmethod
    def list_graphs(
        self,
    ) -> tuple[
        ExperimentLineageGraph,
        ...,
    ]:
        """
        Lists all lineage graphs.
        """

    @abstractmethod
    def exists_graph(
        self,
        *,
        graph_id: str,
    ) -> bool:
        """
        Returns whether a graph exists.
        """