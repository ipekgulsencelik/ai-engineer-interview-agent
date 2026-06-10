from __future__ import annotations

from src.domain.validation.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.metrics.schemas.confidence_interval_schema import (
    CONFIDENCE_INTERVAL_SCHEMA,
)


class ConfidenceIntervalValidator:
    """
    ConfidenceInterval validation service.
    """

    @staticmethod
    def validate(
        *,
        lower_bound: float,
        upper_bound: float,
        confidence_level: float,
    ) -> None:
        SchemaValidator.validate(
            values={
                "lower_bound": lower_bound,
                "upper_bound": upper_bound,
                "confidence_level": confidence_level,
            },
            schema=CONFIDENCE_INTERVAL_SCHEMA,
            error_factory=EvaluationValidationError,
        )

        if upper_bound < lower_bound:
            raise EvaluationValidationError(
                "upper_bound must be greater than or equal to lower_bound."
            )

        if not (
            0.0
            <= confidence_level
            <= 1.0
        ):
            raise EvaluationValidationError(
                "confidence_level must be between 0.0 and 1.0."
            )