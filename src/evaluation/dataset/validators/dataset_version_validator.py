from __future__ import annotations

from src.domain.validators.schema_validator import (
    SchemaValidator,
)
from src.evaluation.dataset.enums.dataset_stage import (
    DatasetStage,
)
from src.evaluation.dataset.schemas.dataset_version_schema import (
    DATASET_VERSION_SCHEMA,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)


class DatasetVersionValidator:
    """
    DatasetVersion validation service.
    """

    @staticmethod
    def validate(
        *,
        version: str,
        stage: DatasetStage,
        created_by: str,
        description: str,
    ) -> None:
        SchemaValidator.validate(
            values={
                "version": version,
                "created_by": created_by,
                "description": description,
            },
            schema=DATASET_VERSION_SCHEMA,
            error_factory=EvaluationValidationError,
        )

        if not isinstance(
            stage,
            DatasetStage,
        ):
            raise EvaluationValidationError(
                "stage must be a DatasetStage enum."
            )