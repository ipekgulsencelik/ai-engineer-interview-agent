from __future__ import annotations

from datetime import datetime

from src.domain.validators.schema_validator import SchemaValidator
from src.evaluation.dataset.schemas.dataset_metadata_schema import DATASET_METADATA_SCHEMA
from src.evaluation.domain.errors.evaluation_validation_error import EvaluationValidationError


class DatasetMetadataValidator:
    """DatasetMetadata validation service."""

    @staticmethod
    def validate(
        *,
        created_at: datetime,
        rubric_version: str,
        evaluator_version: str,
        source: str,
        notes: str | None,
    ) -> None:
        DatasetMetadataValidator._validate_created_at(created_at=created_at)
        SchemaValidator.validate(
            values={
                "rubric_version": rubric_version,
                "evaluator_version": evaluator_version,
                "source": source,
                "notes": notes,
            },
            schema=DATASET_METADATA_SCHEMA,
            error_factory=EvaluationValidationError,
        )

    @staticmethod
    def _validate_created_at(*, created_at: datetime) -> None:
        if not isinstance(created_at, datetime):
            raise EvaluationValidationError("created_at must be a datetime.")
