from __future__ import annotations

from datetime import datetime

from src.domain.validators.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.tracking.enums.lineage_relationship_type import (
    LineageRelationshipType,
)
from src.evaluation.tracking.schemas.lineage_edge_schema import (
    LINEAGE_EDGE_SCHEMA,
)


class LineageEdgeValidator:
    """
    LineageEdge validation service.
    """

    @staticmethod
    def validate(
        *,
        edge_id: str,
        parent_id: str,
        child_id: str,
        relationship_type: LineageRelationshipType,
        created_at: datetime,
        description: str | None,
        metadata: dict[
            str,
            str,
        ] | None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "edge_id": edge_id,
                "parent_id": parent_id,
                "child_id": child_id,
                "relationship_type": str(
                    relationship_type,
                ),
                "created_at": created_at,
                "description": description,
                "metadata": metadata or {},
            },
            schema=LINEAGE_EDGE_SCHEMA,
            error_factory=EvaluationValidationError,
        )

        if not isinstance(
            relationship_type,
            LineageRelationshipType,
        ):
            raise EvaluationValidationError(
                "relationship_type must be LineageRelationshipType."
            )

        if parent_id == child_id:
            raise EvaluationValidationError(
                "parent_id cannot equal child_id."
            )

        if metadata is not None:
            for key, value in metadata.items():
                if not isinstance(
                    key,
                    str,
                ) or not key.strip():
                    raise EvaluationValidationError(
                        "metadata keys must be non-empty strings."
                    )

                if not isinstance(
                    value,
                    str,
                ):
                    raise EvaluationValidationError(
                        "metadata values must be strings."
                    )