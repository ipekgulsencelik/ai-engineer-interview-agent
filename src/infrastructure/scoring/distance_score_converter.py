from __future__ import annotations

from src.infrastructure.constants.scoring_constants import (
    DISTANCE_SCORE_OFFSET,
    MAX_SIMILARITY_SCORE,
    MIN_SIMILARITY_SCORE,
)


class DistanceScoreConverter:
    """
    Converts vector distance into bounded similarity score.
    """

    @staticmethod
    def to_score(
        *,
        distance: float,
    ) -> float:
        score = (
            DISTANCE_SCORE_OFFSET - distance
        )

        return max(
            MIN_SIMILARITY_SCORE,
            min(
                score,
                MAX_SIMILARITY_SCORE,
            ),
        )