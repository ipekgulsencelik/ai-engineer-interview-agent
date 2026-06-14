from __future__ import annotations


class RAGRateCalculator:
    """
    Calculates safe rates.
    """

    @staticmethod
    def calculate(
        *,
        numerator: int,
        denominator: int,
    ) -> float:
        if denominator == 0:
            return 0.0

        return (
            numerator
            / denominator
        )