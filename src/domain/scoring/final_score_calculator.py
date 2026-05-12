from __future__ import annotations

from src.domain.constants.scoring import (
    CV_GAP_SCORE_WEIGHT,
    DIFFICULTY_SCORE_WEIGHT,
    DIVERSITY_SCORE_WEIGHT,
    FATIGUE_SCORE_WEIGHT,
    LEVEL_SCORE_WEIGHT,
    MARKET_SCORE_WEIGHT,
    MAX_SCORE,
    MIN_SCORE,
    TOTAL_SCORE_WEIGHT,
)


class FinalScoreCalculator:
    """
    Weighted final score calculation utility.
    """

    @classmethod
    def compute(
        cls,
        *,
        level_score: float,
        market_score: float,
        cv_gap_score: float,
        difficulty_score: float,
        diversity_score: float,
        fatigue_score: float,
    ) -> float:
        weighted_score = (
            level_score * LEVEL_SCORE_WEIGHT
            + market_score * MARKET_SCORE_WEIGHT
            + cv_gap_score * CV_GAP_SCORE_WEIGHT
            + difficulty_score * DIFFICULTY_SCORE_WEIGHT
            + diversity_score * DIVERSITY_SCORE_WEIGHT
            + fatigue_score * FATIGUE_SCORE_WEIGHT
        )

        normalized_score = cls._normalize(
            weighted_score,
        )

        return cls._clamp(
            normalized_score,
        )

    @staticmethod
    def _normalize(
        score: float,
    ) -> float:
        if TOTAL_SCORE_WEIGHT <= 0:
            return MIN_SCORE

        return score / TOTAL_SCORE_WEIGHT

    @staticmethod
    def _clamp(
        score: float,
    ) -> float:
        return max(
            MIN_SCORE,
            min(
                MAX_SCORE,
                score,
            ),
        )