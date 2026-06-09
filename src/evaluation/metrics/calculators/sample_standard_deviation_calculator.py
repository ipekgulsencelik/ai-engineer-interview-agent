from __future__ import annotations

import math
from collections.abc import Sequence


class SampleStandardDeviationCalculator:
    """
    Sample standard deviation calculator.
    """

    @staticmethod
    def calculate(
        *,
        values: Sequence[float],
    ) -> float:
        mean_value = sum(
            values,
        ) / len(
            values,
        )

        variance = sum(
            (
                value
                - mean_value
            )
            ** 2
            for value in values
        ) / (
            len(values)
            - 1
        )

        return math.sqrt(
            variance,
        )