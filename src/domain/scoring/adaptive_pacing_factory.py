from __future__ import annotations

from src.domain.constants.adaptive_pacing import (
    DEFAULT_DIFFICULTY_MULTIPLIER,
    INCREASE_DIFFICULTY_MULTIPLIER,
    REDUCE_DIFFICULTY_MULTIPLIER,
)
from src.domain.value_objects.adaptive_pacing import (
    AdaptivePacing,
)


class AdaptivePacingFactory:
    """
    AdaptivePacing creation factory.
    """

    @staticmethod
    def stable(
        *,
        target_difficulty: int,
    ) -> AdaptivePacing:
        return AdaptivePacing(
            target_difficulty=target_difficulty,
            difficulty_multiplier=DEFAULT_DIFFICULTY_MULTIPLIER,
            should_reduce_difficulty=False,
            should_increase_difficulty=False,
        )

    @staticmethod
    def increased(
        *,
        target_difficulty: int,
    ) -> AdaptivePacing:
        return AdaptivePacing(
            target_difficulty=target_difficulty,
            difficulty_multiplier=INCREASE_DIFFICULTY_MULTIPLIER,
            should_reduce_difficulty=False,
            should_increase_difficulty=True,
        )

    @staticmethod
    def reduced(
        *,
        target_difficulty: int,
    ) -> AdaptivePacing:
        return AdaptivePacing(
            target_difficulty=target_difficulty,
            difficulty_multiplier=REDUCE_DIFFICULTY_MULTIPLIER,
            should_reduce_difficulty=True,
            should_increase_difficulty=False,
        )