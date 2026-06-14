from __future__ import annotations


class VisualAverageScoreCalculator:
    """
    Calculates average score for visual analytics.
    """

    @staticmethod
    def calculate(
        *,
        scores: tuple[
            float,
            ...,
        ],
    ) -> float | None:
        if not scores:
            return None

        return sum(
            scores,
        ) / len(
            scores,
        )