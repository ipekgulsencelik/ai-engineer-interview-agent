from __future__ import annotations

from src.domain.constants.adaptive_pacing import (
    INCREASE_SCORE_THRESHOLD,
    REDUCE_SCORE_THRESHOLD,
)
from src.domain.pacing.adaptive_pacing_factory import (
    AdaptivePacingFactory,
)
from src.domain.pacing.difficulty_transition_policy import (
    DifficultyTransitionPolicy,
)
from src.domain.value_objects.adaptive_pacing import (
    AdaptivePacing,
)


class AdaptivePacingCalculator:
    """
    Adaptive interview pacing policy.
    """

    @classmethod
    def calculate(
        cls,
        *,
        recent_scores: list[float],
        current_target_difficulty: int,
    ) -> AdaptivePacing:
        if not recent_scores:
            return AdaptivePacingFactory.stable(
                target_difficulty=current_target_difficulty,
            )

        average_score = (
            sum(recent_scores)
            / len(recent_scores)
        )

        if average_score >= INCREASE_SCORE_THRESHOLD:
            return AdaptivePacingFactory.increased(
                target_difficulty=(
                    DifficultyTransitionPolicy.increase(
                        current_difficulty=(
                            current_target_difficulty
                        ),
                    )
                ),
            )

        if average_score <= REDUCE_SCORE_THRESHOLD:
            return AdaptivePacingFactory.reduced(
                target_difficulty=(
                    DifficultyTransitionPolicy.decrease(
                        current_difficulty=(
                            current_target_difficulty
                        ),
                    )
                ),
            )

        return AdaptivePacingFactory.stable(
            target_difficulty=current_target_difficulty,
        )