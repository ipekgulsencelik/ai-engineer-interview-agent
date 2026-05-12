from __future__ import annotations

from src.domain.entities.question import Question
from src.domain.scoring.scoring_context import (
    ScoringContext,
)
from src.domain.policies.weighted_scoring_policy import (
    WeightedScoringPolicy,
)


class WeightedScoringEngineValidator:
    """
    WeightedScoringEngine validation rules.
    """

    @staticmethod
    def validate_policy(
        policy: WeightedScoringPolicy,
    ) -> None:
        if not isinstance(
            policy,
            WeightedScoringPolicy,
        ):
            raise TypeError(
                "policy must be a "
                "WeightedScoringPolicy instance."
            )

    @staticmethod
    def validate_input(
        *,
        question: Question,
        context: ScoringContext,
    ) -> None:
        if not isinstance(question, Question):
            raise TypeError(
                "question must be a "
                "Question instance."
            )

        if not isinstance(
            context,
            ScoringContext,
        ):
            raise TypeError(
                "context must be a "
                "ScoringContext instance."
            )