from __future__ import annotations

from src.evaluation.ops.entities.experiment_lineage_graph import (
    ExperimentLineageGraph,
)
from src.evaluation.ops.entities.experiment_node import (
    ExperimentNode,
)


class ExperimentLineageTraverser:
    """
    Traverses experiment lineage graphs.
    """

    @staticmethod
    def ancestors(
        *,
        graph: ExperimentLineageGraph,
        experiment_id: str,
    ) -> tuple[
        ExperimentNode,
        ...,
    ]:
        ancestors: list[
            ExperimentNode
        ] = []

        current = graph.get_node(
            experiment_id=experiment_id,
        )

        while (
            current is not None
            and current.parent_experiment_id
            is not None
        ):
            parent = graph.get_node(
                experiment_id=(
                    current.parent_experiment_id
                ),
            )

            if parent is None:
                break

            ancestors.append(
                parent,
            )

            current = parent

        return tuple(
            ancestors,
        )

    @staticmethod
    def descendants(
        *,
        graph: ExperimentLineageGraph,
        experiment_id: str,
    ) -> tuple[
        ExperimentNode,
        ...,
    ]:
        descendants: list[
            ExperimentNode
        ] = []

        stack = list(
            graph.get_children(
                experiment_id=experiment_id,
            )
        )

        while stack:
            node = stack.pop()

            descendants.append(
                node,
            )

            stack.extend(
                graph.get_children(
                    experiment_id=(
                        node.experiment_id
                    ),
                )
            )

        return tuple(
            descendants,
        )

    @staticmethod
    def path_to_root(
        *,
        graph: ExperimentLineageGraph,
        experiment_id: str,
    ) -> tuple[
        ExperimentNode,
        ...,
    ]:
        node = graph.get_node(
            experiment_id=experiment_id,
        )

        if node is None:
            return ()

        return (
            node,
            *ExperimentLineageTraverser.ancestors(
                graph=graph,
                experiment_id=experiment_id,
            ),
        )