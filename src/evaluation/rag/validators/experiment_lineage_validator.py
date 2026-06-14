from __future__ import annotations

from src.evaluation.rag.entities.experiment_lineage_graph import (
    ExperimentLineageGraph,
)
from src.evaluation.rag.entities.experiment_node import (
    ExperimentNode,
)


class ExperimentLineageValidator:
    """
    Validates experiment lineage graph mutation rules.
    """

    @staticmethod
    def validate_node_exists(
        *,
        graph: ExperimentLineageGraph,
        experiment_id: str,
    ) -> None:
        if graph.get_node(
            experiment_id=experiment_id,
        ) is None:
            raise ValueError(
                "experiment node does not exist: "
                f"{experiment_id}"
            )

    @staticmethod
    def validate_node_does_not_exist(
        *,
        graph: ExperimentLineageGraph,
        experiment_id: str,
    ) -> None:
        if graph.get_node(
            experiment_id=experiment_id,
        ) is not None:
            raise ValueError(
                "experiment node already exists: "
                f"{experiment_id}"
            )

    @classmethod
    def validate_nodes_do_not_exist(
        cls,
        *,
        graph: ExperimentLineageGraph,
        nodes: tuple[
            ExperimentNode,
            ...,
        ],
    ) -> None:
        duplicated_existing_ids = tuple(
            node.experiment_id
            for node in nodes
            if graph.get_node(
                experiment_id=node.experiment_id,
            )
            is not None
        )

        if duplicated_existing_ids:
            raise ValueError(
                "experiment nodes already exist: "
                f"{duplicated_existing_ids}"
            )

        incoming_ids = tuple(
            node.experiment_id
            for node in nodes
        )

        repeated_incoming_ids = tuple(
            sorted(
                {
                    experiment_id
                    for experiment_id in incoming_ids
                    if incoming_ids.count(
                        experiment_id,
                    )
                    > 1
                }
            )
        )

        if repeated_incoming_ids:
            raise ValueError(
                "duplicate experiment nodes in input: "
                f"{repeated_incoming_ids}"
            )

    @staticmethod
    def validate_root_is_not_removed(
        *,
        graph: ExperimentLineageGraph,
        experiment_id: str,
    ) -> None:
        if graph.root_experiment_id == experiment_id:
            raise ValueError(
                "root experiment node cannot be removed."
            )