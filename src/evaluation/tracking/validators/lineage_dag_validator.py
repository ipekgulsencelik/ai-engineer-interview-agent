from __future__ import annotations

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.tracking.entities.experiment_node import (
    ExperimentNode,
)
from src.evaluation.tracking.entities.lineage_edge import (
    LineageEdge,
)


class LineageDAGValidator:
    """
    Validates experiment lineage DAG structure.
    """

    def validate(
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
        ],
    ) -> None:
        if not nodes:
            raise EvaluationValidationError(
                "nodes cannot be empty."
            )

        node_ids = {
            node.experiment_id
            for node in nodes
        }

        if root_experiment_id not in node_ids:
            raise EvaluationValidationError(
                "root_experiment_id must exist in nodes."
            )

        self._validate_edges_reference_existing_nodes(
            edges=edges,
            node_ids=node_ids,
        )

        self._validate_single_parent_per_child(
            edges=edges,
        )

        self._validate_acyclic(
            nodes=nodes,
            edges=edges,
        )

    @staticmethod
    def _validate_edges_reference_existing_nodes(
        *,
        edges: tuple[
            LineageEdge,
            ...,
        ],
        node_ids: set[
            str,
        ],
    ) -> None:
        for edge in edges:
            if edge.parent_id not in node_ids:
                raise EvaluationValidationError(
                    "edge parent_id must reference an existing node."
                )

            if edge.child_id not in node_ids:
                raise EvaluationValidationError(
                    "edge child_id must reference an existing node."
                )

    @staticmethod
    def _validate_single_parent_per_child(
        *,
        edges: tuple[
            LineageEdge,
            ...,
        ],
    ) -> None:
        seen_children: set[
            str,
        ] = set()

        for edge in edges:
            if edge.child_id in seen_children:
                raise EvaluationValidationError(
                    "each child node can have only one parent."
                )

            seen_children.add(
                edge.child_id,
            )

    @staticmethod
    def _validate_acyclic(
        *,
        nodes: tuple[
            ExperimentNode,
            ...,
        ],
        edges: tuple[
            LineageEdge,
            ...,
        ],
    ) -> None:
        parent_by_child = {
            edge.child_id: edge.parent_id
            for edge in edges
        }

        for node in nodes:
            visited: set[
                str,
            ] = set()

            current_id: str | None = (
                node.experiment_id
            )

            while current_id is not None:
                if current_id in visited:
                    raise EvaluationValidationError(
                        "lineage DAG cannot contain cycles."
                    )

                visited.add(
                    current_id,
                )

                current_id = parent_by_child.get(
                    current_id,
                )