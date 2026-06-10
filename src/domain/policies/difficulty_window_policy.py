from __future__ import annotations

from src.domain.constants.interview_state import (
    DIFFICULTY_WINDOW_SIZE,
    MAX_TARGET_DIFFICULTY,
    MIN_TARGET_DIFFICULTY,
)


class DifficultyWindowPolicy:
    """
    Difficulty range window policy.
    """

    @staticmethod
    def minimum(
        *,
        target_difficulty: int,
    ) -> int:
        return max(
            target_difficulty
            - DIFFICULTY_WINDOW_SIZE,
            MIN_TARGET_DIFFICULTY,
        )

    @staticmethod
    def maximum(
        *,
        target_difficulty: int,
    ) -> int:
        return min(
            target_difficulty
            + DIFFICULTY_WINDOW_SIZE,
            MAX_TARGET_DIFFICULTY,
        )