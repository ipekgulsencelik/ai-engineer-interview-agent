from __future__ import annotations

from uuid import uuid4

from src.evaluation.tracking.entities.experiment_lineage_graph import (
    ExperimentLineageGraph,
)
from src.evaluation.tracking.entities.experiment_node import (
    ExperimentNode,
)
from src.evaluation.tracking.entities.lineage_edge import (
    LineageEdge,
)
from src.evaluation.tracking.services.lineage_edge_applier import (
    LineageEdgeApplier,
)
from src.evaluation.tracking.validators.lineage_dag_validator import (
    LineageDAGValidator,
)


class LineageDAGBuilder:
    """
    Builds experiment lineage DAGs from nodes and edges.
    """

    def __init__(
        self,
        *,
        edge_applier: LineageEdgeApplier | None = None,
        validator: LineageDAGValidator | None = None,
    ) -> None:
        self._edge_applier = (
            edge_applier
            or LineageEdgeApplier()
        )
        self._validator = (
            validator
            or LineageDAGValidator()
        )

    def build(
        self,
        *,
        root_experiment_id: str,
        nodes: tuple[
            ExperimentNode,
            ...,
        ],
        edges: tuple[
            LineageEdge,
            ...,
        ] = (),
        notes: str | None = None,
    ) -> ExperimentLineageGraph:
        self._validator.validate(
            root_experiment_id=root_experiment_id,
            nodes=nodes,
            edges=edges,
        )

        return ExperimentLineageGraph(
            graph_id=str(
                uuid4(),
            ),
            root_experiment_id=root_experiment_id,
            nodes=self._edge_applier.apply(
                nodes=nodes,
                edges=edges,
            ),
            notes=notes,
        )