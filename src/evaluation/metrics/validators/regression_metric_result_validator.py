from __future__ import annotations

from src.domain.validators.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.metrics.schemas.regression_metric_result_schema import (
    REGRESSION_METRIC_RESULT_SCHEMA,
)


class RegressionMetricResultValidator:
    """
    RegressionMetricResult validation service.
    """

    @staticmethod
    def validate(
        *,
        metric_name: str,
        mae: float,
        mse: float,
        rmse: float,
        r2_score: float,
        sample_count: int,
        is_acceptable: bool,
        interpretation: str,
        notes: str | None = None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "metric_name": metric_name,
                "mae": mae,
                "mse": mse,
                "rmse": rmse,
                "r2_score": r2_score,
                "sample_count": sample_count,
                "is_acceptable": is_acceptable,
                "interpretation": interpretation,
                "notes": notes,
            },
            schema=REGRESSION_METRIC_RESULT_SCHEMA,
            error_factory=EvaluationValidationError,
        )