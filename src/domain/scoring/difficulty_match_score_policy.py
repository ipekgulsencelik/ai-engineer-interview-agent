from __future__ import annotations

from src.domain.constants.retrieval_scoring import (
    DIFFICULTY_DISTANCE_NORMALIZER,
    NORMALIZED_SCORE_BASE,
)
from src.domain.scoring.normalized_score_clamper import (
    NormalizedScoreClamper,
)


class DifficultyMatchScorePolicy:
    """
    Question difficulty and target difficulty compatibility policy.
    """

    @staticmethod
    def calculate(
        *,
        question_difficulty: int,
        target_difficulty: int,
    ) -> float:
        distance = abs(
            question_difficulty
            - target_difficulty,
        )

        score = (
            NORMALIZED_SCORE_BASE
            - (
                distance
                / DIFFICULTY_DISTANCE_NORMALIZER
            )
        )

        return NormalizedScoreClamper.clamp(
            score=score,
        )