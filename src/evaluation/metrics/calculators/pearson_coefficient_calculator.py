from __future__ import annotations

import math
from collections.abc import Sequence

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.metrics.constants.correlations import (
    ZERO_DENOMINATOR_THRESHOLD,
)


class PearsonCoefficientCalculator:
    """
    Pearson coefficient calculator.

    Calculates Pearson's r for validated numeric series.
    """

    @staticmethod
    def calculate(
        *,
        x_values: Sequence[float],
        y_values: Sequence[float],
    ) -> float:
        x_mean = sum(x_values) / len(x_values)
        y_mean = sum(y_values) / len(y_values)

        numerator = sum(
            (
                x_value
                - x_mean
            )
            * (
                y_value
                - y_mean
            )
            for x_value, y_value in zip(
                x_values,
                y_values,
                strict=True,
            )
        )

        x_denominator = math.sqrt(
            sum(
                (
                    x_value
                    - x_mean
                )
                ** 2
                for x_value in x_values
            )
        )

        y_denominator = math.sqrt(
            sum(
                (
                    y_value
                    - y_mean
                )
                ** 2
                for y_value in y_values
            )
        )

        denominator = (
            x_denominator
            * y_denominator
        )

        if abs(denominator) < ZERO_DENOMINATOR_THRESHOLD:
            raise EvaluationValidationError(
                "Pearson correlation is undefined for constant values."
            )

        return numerator / denominator