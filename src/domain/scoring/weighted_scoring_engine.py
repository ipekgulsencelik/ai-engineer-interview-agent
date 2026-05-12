from __future__ import annotations

from src.application.ports.scoring_engine import (
    ScoringEngine,
)
from src.domain.entities.question import Question
from src.domain.scoring.scoring_breakdown import (
    ScoringBreakdown,
)
from src.domain.scoring.scoring_context import (
    ScoringContext,
)
from src.domain.validators.weighted_scoring_engine_validator import (
    WeightedScoringEngineValidator,
)
from src.domain.scoring.weighted_scoring_policy import (
    WeightedScoringPolicy,
)


class WeightedScoringEngine(ScoringEngine):
    """
    Weighted explainable scoring engine.
    """

    def __init__(
        self,
        policy: WeightedScoringPolicy,
    ) -> None:
        WeightedScoringEngineValidator.validate_policy(
            policy,
        )

        self._policy = policy

    def score(
        self,
        *,
        question: Question,
        context: ScoringContext,
    ) -> ScoringBreakdown:
        WeightedScoringEngineValidator.validate_input(
            question=question,
            context=context,
        )

        level_score = self._policy.compute_level_score(
            question=question,
            context=context,
        )

        market_score = self._policy.compute_market_score(
            question=question,
            context=context,
        )

        cv_gap_score = self._policy.compute_cv_gap_score(
            question=question,
            context=context,
        )

        difficulty_score = (
            self._policy.compute_difficulty_score(
                question=question,
                context=context,
            )
        )

        diversity_score = (
            self._policy.compute_diversity_score(
                question=question,
                context=context,
            )
        )

        fatigue_score = (
            self._policy.compute_fatigue_score(
                question=question,
                context=context,
            )
        )

        final_score = self._policy.compute_final_score(
            level_score=level_score,
            market_score=market_score,
            cv_gap_score=cv_gap_score,
            difficulty_score=difficulty_score,
            diversity_score=diversity_score,
            fatigue_score=fatigue_score,
        )

        return ScoringBreakdown(
            level_score=level_score,
            market_score=market_score,
            cv_gap_score=cv_gap_score,
            difficulty_score=difficulty_score,
            diversity_score=diversity_score,
            fatigue_score=fatigue_score,
            final_score=final_score,
        )