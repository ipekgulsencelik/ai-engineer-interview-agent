from __future__ import annotations

from src.evaluation.metrics.constants.alignment import (
    ALIGNMENT_METRIC_COUNT,
    MAX_ALIGNMENT_SCORE,
    MIN_ALIGNMENT_SCORE,
)


class OverallAlignmentScoreCalculator:
    """
    Aggregates correlation, agreement, and regression scores
    into a normalized overall alignment score.
    """

    @staticmethod
    def calculate(
        *,
        correlation_score: float,
        agreement_score: float,
        regression_score: float,
    ) -> float:
        normalized_regression_score = (
            OverallAlignmentScoreCalculator._clamp_score(
                score=regression_score,
            )
        )

        return (
            correlation_score
            + agreement_score
            + normalized_regression_score
        ) / ALIGNMENT_METRIC_COUNT

    @staticmethod
    def _clamp_score(
        *,
        score: float,
    ) -> float:
        return max(
            MIN_ALIGNMENT_SCORE,
            min(
                MAX_ALIGNMENT_SCORE,
                score,
            ),
        )