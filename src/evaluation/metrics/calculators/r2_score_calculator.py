from __future__ import annotations

from collections.abc import Sequence

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.metrics.constants.regression_metrics import (
    ZERO_TOTAL_VARIANCE_THRESHOLD,
)


class R2ScoreCalculator:
    """
    R² score calculator.
    """

    @staticmethod
    def calculate(
        *,
        actual_values: Sequence[float],
        predicted_values: Sequence[float],
    ) -> float:
        actual_mean = sum(
            actual_values,
        ) / len(
            actual_values,
        )

        total_sum_of_squares = sum(
            (
                actual
                - actual_mean
            )
            ** 2
            for actual in actual_values
        )

        if abs(
            total_sum_of_squares,
        ) < ZERO_TOTAL_VARIANCE_THRESHOLD:
            raise EvaluationValidationError(
                "R2 score is undefined when actual values are constant."
            )

        residual_sum_of_squares = sum(
            (
                actual
                - predicted
            )
            ** 2
            for actual, predicted in zip(
                actual_values,
                predicted_values,
                strict=True,
            )
        )

        return 1.0 - (
            residual_sum_of_squares
            / total_sum_of_squares
        )