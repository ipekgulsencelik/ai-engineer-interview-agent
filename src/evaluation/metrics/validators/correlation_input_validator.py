from __future__ import annotations

import math
from collections.abc import Sequence

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.metrics.constants.correlations import (
    MIN_CORRELATION_SAMPLE_COUNT,
)


class CorrelationInputValidator:
    """
    Correlation input validation service.
    """

    @staticmethod
    def validate(
        *,
        x_values: Sequence[float],
        y_values: Sequence[float],
    ) -> None:
        if len(x_values) != len(y_values):
            raise EvaluationValidationError(
                "x_values and y_values must have the same length."
            )

        if len(x_values) < MIN_CORRELATION_SAMPLE_COUNT:
            raise EvaluationValidationError(
                "correlation requires at least "
                f"{MIN_CORRELATION_SAMPLE_COUNT} values."
            )

        CorrelationInputValidator._validate_numeric_series(
            values=x_values,
            field_name="x_values",
        )

        CorrelationInputValidator._validate_numeric_series(
            values=y_values,
            field_name="y_values",
        )

    @staticmethod
    def _validate_numeric_series(
        *,
        values: Sequence[float],
        field_name: str,
    ) -> None:
        for index, value in enumerate(values):
            if (
                isinstance(value, bool)
                or not isinstance(
                    value,
                    (int, float),
                )
            ):
                raise EvaluationValidationError(
                    f"{field_name}[{index}] must be numeric."
                )

            if not math.isfinite(
                float(value),
            ):
                raise EvaluationValidationError(
                    f"{field_name}[{index}] must be finite."
                )