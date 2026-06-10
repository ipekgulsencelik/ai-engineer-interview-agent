from __future__ import annotations


class RegressionScoreDeltaCalculator:
    """
    Calculates score delta between baseline and candidate scores.
    """

    @staticmethod
    def calculate(
        *,
        baseline_score: float,
        candidate_score: float,
    ) -> float:
        return (
            candidate_score
            - baseline_score
        )