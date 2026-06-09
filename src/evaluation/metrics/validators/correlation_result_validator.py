from __future__ import annotations

from src.domain.validators.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.metrics.schemas.correlation_result_schema import (
    CORRELATION_RESULT_SCHEMA,
)


class CorrelationResultValidator:
    """
    CorrelationResult validation service.
    """

    @staticmethod
    def validate(
        *,
        metric_x: str,
        metric_y: str,
        correlation_coefficient: float,
        p_value: float,
        sample_count: int,
        method: str,
        is_significant: bool,
        notes: str | None = None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "metric_x": metric_x,
                "metric_y": metric_y,
                "correlation_coefficient": correlation_coefficient,
                "p_value": p_value,
                "sample_count": sample_count,
                "method": method,
                "is_significant": is_significant,
                "notes": notes,
            },
            schema=CORRELATION_RESULT_SCHEMA,
            error_factory=EvaluationValidationError,
        )