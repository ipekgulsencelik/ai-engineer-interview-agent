from __future__ import annotations

from src.domain.validators.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.rag.entities.experiment_node import (
    ExperimentNode,
)
from src.evaluation.rag.schemas.experiment_lineage_graph_schema import (
    EXPERIMENT_LINEAGE_GRAPH_SCHEMA,
)


class ExperimentLineageGraphValidator:
    """
    ExperimentLineageGraph validation service.
    """

    @staticmethod
    def validate(
        *,
        graph_id: str,
        root_experiment_id: str,
        nodes: tuple[
            ExperimentNode,
            ...,
        ],
        notes: str | None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "graph_id": graph_id,
                "root_experiment_id": root_experiment_id,
                "nodes": nodes,
                "notes": notes,
            },
            schema=EXPERIMENT_LINEAGE_GRAPH_SCHEMA,
            error_factory=EvaluationValidationError,
        )

        experiment_ids = {
            node.experiment_id
            for node in nodes
        }

        if root_experiment_id not in experiment_ids:
            raise EvaluationValidationError(
                "root_experiment_id must exist in nodes."
            )

        for index, node in enumerate(
            nodes,
        ):
            if not isinstance(
                node,
                ExperimentNode,
            ):
                raise EvaluationValidationError(
                    f"nodes[{index}] must be ExperimentNode."
                )

        if len(experiment_ids) != len(nodes):
            raise EvaluationValidationError(
                "experiment ids must be unique."
            )

        for node in nodes:
            if (
                node.parent_experiment_id is not None
                and node.parent_experiment_id
                not in experiment_ids
            ):
                raise EvaluationValidationError(
                    "parent_experiment_id must reference an existing node."
                )

        ExperimentLineageGraphValidator._validate_acyclic(
            nodes=nodes,
        )

    @staticmethod
    def _validate_acyclic(
        *,
        nodes: tuple[
            ExperimentNode,
            ...,
        ],
    ) -> None:
        parent_by_id = {
            node.experiment_id: node.parent_experiment_id
            for node in nodes
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
                        "experiment lineage graph cannot contain cycles."
                    )

                visited.add(
                    current_id,
                )

                current_id = parent_by_id.get(
                    current_id,
                )