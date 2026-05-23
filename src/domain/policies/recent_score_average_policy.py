from __future__ import annotations

from src.domain.constants.level_transition import (
    MIN_REQUIRED_RECENT_SCORES,
)
from src.domain.errors.level_transition_error import (
    LevelTransitionError,
)


class RecentScoreAveragePolicy:
    """
    Recent score aggregation policy.
    """

    @staticmethod
    def calculate(
        *,
        scores: list[float],
    ) -> float:
        if len(scores) < MIN_REQUIRED_RECENT_SCORES:
            raise LevelTransitionError(
                "scores cannot be empty."
            )

        return sum(scores) / len(scores)