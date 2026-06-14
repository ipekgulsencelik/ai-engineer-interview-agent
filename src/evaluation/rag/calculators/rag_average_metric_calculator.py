from __future__ import annotations


class RAGAverageMetricCalculator:
    """
    Calculates average metric values.
    """

    @staticmethod
    def calculate(
        *,
        values: tuple[
            float,
            ...,
        ],
    ) -> float:
        if not values:
            return 0.0

        return sum(
            values,
        ) / len(
            values,
        )