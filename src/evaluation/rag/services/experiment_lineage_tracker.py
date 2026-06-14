from __future__ import annotations

from src.evaluation.rag.builders.experiment_lineage_builder import (
    ExperimentLineageBuilder,
)
from src.evaluation.rag.entities.experiment_lineage_graph import (
    ExperimentLineageGraph,
)
from src.evaluation.rag.entities.experiment_node import (
    ExperimentNode,
)
from src.evaluation.rag.validators.experiment_lineage_validator import (
    ExperimentLineageValidator,
)


class ExperimentLineageTracker:
    """
    Tracks experiment lineage by composing experiment
    nodes into immutable lineage graphs.
    """

    def __init__(
        self,
        *,
        lineage_builder: ExperimentLineageBuilder | None = None,
        lineage_validator: ExperimentLineageValidator | None = None,
    ) -> None:
        self._lineage_builder = (
            lineage_builder
            or ExperimentLineageBuilder()
        )
        self._lineage_validator = (
            lineage_validator
            or ExperimentLineageValidator()
        )

    def create_graph(
        self,
        *,
        root_node: ExperimentNode,
        child_nodes: tuple[
            ExperimentNode,
            ...,
        ] = (),
        notes: str | None = None,
    ) -> ExperimentLineageGraph:
        self._lineage_validator.validate_unique_nodes(
            nodes=(root_node, *child_nodes),
        )

        return self._lineage_builder.build(
            root_experiment_id=root_node.experiment_id,
            nodes=(
                root_node,
                *child_nodes,
            ),
            notes=notes,
        )

    def append_node(
        self,
        *,
        graph: ExperimentLineageGraph,
        node: ExperimentNode,
    ) -> ExperimentLineageGraph:
        self._lineage_validator.validate_node_does_not_exist(
            graph=graph,
            experiment_id=node.experiment_id,
        )

        return self._lineage_builder.build(
            root_experiment_id=graph.root_experiment_id,
            nodes=(
                *graph.nodes,
                node,
            ),
            notes=graph.notes,
        )

    def append_nodes(
        self,
        *,
        graph: ExperimentLineageGraph,
        nodes: tuple[
            ExperimentNode,
            ...,
        ],
    ) -> ExperimentLineageGraph:
        self._lineage_validator.validate_nodes_do_not_exist(
            graph=graph,
            nodes=nodes,
        )

        return self._lineage_builder.build(
            root_experiment_id=graph.root_experiment_id,
            nodes=(
                *graph.nodes,
                *nodes,
            ),
            notes=graph.notes,
        )

    def replace_node(
        self,
        *,
        graph: ExperimentLineageGraph,
        node: ExperimentNode,
    ) -> ExperimentLineageGraph:
        self._lineage_validator.validate_node_exists(
            graph=graph,
            experiment_id=node.experiment_id,
        )

        updated_nodes = tuple(
            node
            if existing.experiment_id == node.experiment_id
            else existing
            for existing in graph.nodes
        )

        return self._lineage_builder.build(
            root_experiment_id=graph.root_experiment_id,
            nodes=updated_nodes,
            notes=graph.notes,
        )

    def remove_node(
        self,
        *,
        graph: ExperimentLineageGraph,
        experiment_id: str,
    ) -> ExperimentLineageGraph:
        self._lineage_validator.validate_node_exists(
            graph=graph,
            experiment_id=experiment_id,
        )

        self._lineage_validator.validate_root_is_not_removed(
            graph=graph,
            experiment_id=experiment_id,
        )

        updated_nodes = tuple(
            node
            for node in graph.nodes
            if node.experiment_id != experiment_id
        )

        return self._lineage_builder.build(
            root_experiment_id=graph.root_experiment_id,
            nodes=updated_nodes,
            notes=graph.notes,
        )