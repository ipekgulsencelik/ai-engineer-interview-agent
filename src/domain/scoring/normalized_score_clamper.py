from __future__ import annotations

from src.domain.constants.retrieval_scoring import (
    MAX_NORMALIZED_SCORE,
    MIN_NORMALIZED_SCORE,
)


class NormalizedScoreClamper:
    """
    Clamp helper for normalized scores.
    """

    def __new__(cls) -> "NormalizedScoreClamper":
        raise TypeError(
            "NormalizedScoreClamper cannot be instantiated."
        )

    @staticmethod
    def clamp(
        *,
        score: float,
    ) -> float:
        return max(
            MIN_NORMALIZED_SCORE,
            min(
                score,
                MAX_NORMALIZED_SCORE,
            ),
        )