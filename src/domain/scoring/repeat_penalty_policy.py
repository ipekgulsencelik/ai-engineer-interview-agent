from __future__ import annotations

from src.domain.constants.diversity_scoring import (
    MAX_REPEAT_PENALTY,
    REPEAT_PENALTY_STEP,
)


class RepeatPenaltyPolicy:
    """
    Repeat-based diversity penalty policy.
    """

    @staticmethod
    def calculate(
        *,
        repeat_count: int,
    ) -> float:
        raw_penalty = (
            repeat_count
            * REPEAT_PENALTY_STEP
        )

        return min(
            raw_penalty,
            MAX_REPEAT_PENALTY,
        )