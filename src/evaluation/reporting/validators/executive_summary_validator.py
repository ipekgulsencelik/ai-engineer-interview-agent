from __future__ import annotations

from src.domain.validators.schema_validator import SchemaValidator
from src.evaluation.domain.errors.evaluation_validation_error import EvaluationValidationError
from src.evaluation.reporting.schemas.executive_summary_schema import EXECUTIVE_SUMMARY_SCHEMA


class ExecutiveSummaryValidator:
    """ExecutiveSummary validation service."""

    @staticmethod
    def validate(**values: object) -> None:
        SchemaValidator.validate(
            values=dict(values),
            schema=EXECUTIVE_SUMMARY_SCHEMA,
            error_factory=EvaluationValidationError,
        )
