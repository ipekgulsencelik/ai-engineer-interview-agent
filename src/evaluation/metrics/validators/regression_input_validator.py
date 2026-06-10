from __future__ import annotations

import math
from collections.abc import Sequence

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.metrics.constants.regression_metrics import (
    MIN_REGRESSION_SAMPLE_COUNT,
)


class RegressionInputValidator:
    """
    Regression metric input validation service.
    """

    @staticmethod
    def validate(
        *,
        actual_values: Sequence[float],
        predicted_values: Sequence[float],
    ) -> None:
        if len(actual_values) != len(predicted_values):
            raise EvaluationValidationError(
                "actual_values and predicted_values must have the same length."
            )

        if len(actual_values) < MIN_REGRESSION_SAMPLE_COUNT:
            raise EvaluationValidationError(
                "regression metrics require at least "
                f"{MIN_REGRESSION_SAMPLE_COUNT} value."
            )

        RegressionInputValidator._validate_numeric_series(
            values=actual_values,
            field_name="actual_values",
        )

        RegressionInputValidator._validate_numeric_series(
            values=predicted_values,
            field_name="predicted_values",
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