from __future__ import annotations

from uuid import uuid4

from src.evaluation.rag.entities.experiment_lineage_graph import (
    ExperimentLineageGraph,
)
from src.evaluation.rag.entities.experiment_node import (
    ExperimentNode,
)


class ExperimentLineageBuilder:
    """
    Builds experiment lineage graphs from nodes.
    """

    @staticmethod
    def build(
        *,
        root_experiment_id: str,
        nodes: tuple[
            ExperimentNode,
            ...,
        ],
        notes: str | None = None,
    ) -> ExperimentLineageGraph:
        return ExperimentLineageGraph(
            graph_id=str(
                uuid4(),
            ),
            root_experiment_id=(
                root_experiment_id
            ),
            nodes=nodes,
            notes=notes,
        )