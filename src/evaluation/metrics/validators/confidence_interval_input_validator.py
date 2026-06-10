from __future__ import annotations

import math
from collections.abc import Sequence

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.metrics.constants.confidence_intervals import (
    MAX_CONFIDENCE_LEVEL,
    MIN_CONFIDENCE_LEVEL,
    MIN_CONFIDENCE_SAMPLE_COUNT,
    MIN_Z_SCORE,
)


class ConfidenceIntervalInputValidator:
    """
    Confidence interval input validation service.
    """

    @staticmethod
    def validate(
        *,
        values: Sequence[float],
        confidence_level: float,
        z_score: float,
    ) -> None:
        if (
            len(values)
            < MIN_CONFIDENCE_SAMPLE_COUNT
        ):
            raise EvaluationValidationError(
                "values cannot be empty."
            )

        for index, value in enumerate(values):
            if (
                isinstance(value, bool)
                or not isinstance(
                    value,
                    (
                        int,
                        float,
                    ),
                )
            ):
                raise EvaluationValidationError(
                    f"values[{index}] must be numeric."
                )

            if not math.isfinite(
                float(value),
            ):
                raise EvaluationValidationError(
                    f"values[{index}] must be finite."
                )

        if not (
            MIN_CONFIDENCE_LEVEL
            < confidence_level
            < MAX_CONFIDENCE_LEVEL
        ):
            raise EvaluationValidationError(
                "confidence_level must be between 0 and 1."
            )

        if z_score <= MIN_Z_SCORE:
            raise EvaluationValidationError(
                "z_score must be positive."
            )