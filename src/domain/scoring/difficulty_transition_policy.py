from __future__ import annotations

from src.domain.constants.adaptive_pacing import (
    DIFFICULTY_STEP,
    MAX_TARGET_DIFFICULTY,
    MIN_TARGET_DIFFICULTY,
)


class DifficultyTransitionPolicy:
    """
    Difficulty transition policy.
    """

    @staticmethod
    def increase(
        *,
        current_difficulty: int,
    ) -> int:
        return min(
            current_difficulty
            + DIFFICULTY_STEP,
            MAX_TARGET_DIFFICULTY,
        )

    @staticmethod
    def decrease(
        *,
        current_difficulty: int,
    ) -> int:
        return max(
            current_difficulty
            - DIFFICULTY_STEP,
            MIN_TARGET_DIFFICULTY,
        )