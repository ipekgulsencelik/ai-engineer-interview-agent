from __future__ import annotations

from datetime import datetime

from src.domain.validation.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.ops.schemas.experiment_tag_schema import (
    EXPERIMENT_TAG_SCHEMA,
)


class ExperimentTagValidator:
    """
    ExperimentTag validation service.
    """

    @staticmethod
    def validate(
        *,
        tag_id: str,
        key: str,
        value: str,
        created_at: datetime,
        description: str | None,
        created_by: str | None,
        metadata: dict[
            str,
            str,
        ] | None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "tag_id": tag_id,
                "key": key,
                "value": value,
                "created_at": created_at,
                "description": description,
                "created_by": created_by,
                "metadata": metadata or {},
            },
            schema=EXPERIMENT_TAG_SCHEMA,
            error_factory=EvaluationValidationError,
        )

        if key.startswith(".") or key.endswith("."):
            raise EvaluationValidationError(
                "key cannot start or end with '.'."
            )

        if ".." in key:
            raise EvaluationValidationError(
                "key cannot contain consecutive dots."
            )

        if metadata is not None:
            for metadata_key, metadata_value in metadata.items():
                if not isinstance(
                    metadata_key,
                    str,
                ) or not metadata_key.strip():
                    raise EvaluationValidationError(
                        "metadata keys must be non-empty strings."
                    )

                if not isinstance(
                    metadata_value,
                    str,
                ):
                    raise EvaluationValidationError(
                        "metadata values must be strings."
                    )