from __future__ import annotations

from collections.abc import Sequence


class MAECalculator:
    """
    Mean absolute error calculator.
    """

    @staticmethod
    def calculate(
        *,
        actual_values: Sequence[float],
        predicted_values: Sequence[float],
    ) -> float:
        return sum(
            abs(
                actual
                - predicted,
            )
            for actual, predicted in zip(
                actual_values,
                predicted_values,
                strict=True,
            )
        ) / len(actual_values)