from __future__ import annotations

from src.domain.validation.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.metrics.schemas.trend_data_point_schema import (
    TREND_DATA_POINT_SCHEMA,
)


class TrendDataPointValidator:
    """
    TrendDataPoint validation service.
    """

    @staticmethod
    def validate(
        *,
        label: str,
        value: float,
    ) -> None:
        SchemaValidator.validate(
            values={
                "label": label,
                "value": value,
            },
            schema=TREND_DATA_POINT_SCHEMA,
            error_factory=EvaluationValidationError,
        )