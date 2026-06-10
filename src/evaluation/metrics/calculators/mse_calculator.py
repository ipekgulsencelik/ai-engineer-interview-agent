from __future__ import annotations

from collections.abc import Sequence


class MSECalculator:
    """
    Mean squared error calculator.
    """

    @staticmethod
    def calculate(
        *,
        actual_values: Sequence[float],
        predicted_values: Sequence[float],
    ) -> float:
        return sum(
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
        ) / len(actual_values)