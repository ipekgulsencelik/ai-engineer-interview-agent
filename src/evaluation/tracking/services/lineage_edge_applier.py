from __future__ import annotations

from dataclasses import replace

from src.evaluation.tracking.entities.experiment_node import (
    ExperimentNode,
)
from src.evaluation.tracking.entities.lineage_edge import (
    LineageEdge,
)


class LineageEdgeApplier:
    """
    Applies lineage edges to experiment nodes.
    """

    def apply(
        self,
        *,
        nodes: tuple[
            ExperimentNode,
            ...,
        ],
        edges: tuple[
            LineageEdge,
            ...,
        ],
    ) -> tuple[
        ExperimentNode,
        ...,
    ]:
        if not edges:
            return nodes

        parent_by_child = {
            edge.child_id: edge.parent_id
            for edge in edges
        }

        return tuple(
            self._with_parent(
                node=node,
                parent_by_child=parent_by_child,
            )
            for node in nodes
        )

    @staticmethod
    def _with_parent(
        *,
        node: ExperimentNode,
        parent_by_child: dict[
            str,
            str,
        ],
    ) -> ExperimentNode:
        parent_id = parent_by_child.get(
            node.experiment_id,
        )

        if parent_id is None:
            return node

        return replace(
            node,
            parent_experiment_id=parent_id,
        )