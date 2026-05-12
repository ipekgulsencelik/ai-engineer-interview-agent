from __future__ import annotations

from src.domain.entities.question import Question
from src.domain.policies.cv_gap_score_policy import (
    CvGapScorePolicy,
)
from src.domain.policies.level_score_policy import (
    LevelScorePolicy,
)
from src.domain.policies.market_score_policy import (
    MarketScorePolicy,
)
from src.domain.policies.difficulty_score_policy import (
    DifficultyScorePolicy,
)
from src.domain.policies.diversity_score_policy import (
    DiversityScorePolicy,
)
from src.domain.policies.fatigue_score_policy import (
    FatigueScorePolicy,
)
from src.domain.scoring.scoring_context import ScoringContext


class WeightedScoringPolicy:
    """
    Composite scoring policy.
    """

    def __init__(
        self,
        *,
        level_score_policy: LevelScorePolicy,
        market_score_policy: MarketScorePolicy,
        cv_gap_score_policy: CvGapScorePolicy,
        difficulty_score_policy: DifficultyScorePolicy,
        diversity_score_policy: DiversityScorePolicy,
        fatigue_score_policy: FatigueScorePolicy,
    ) -> None:
        self._level_score_policy = level_score_policy
        self._market_score_policy = market_score_policy
        self._cv_gap_score_policy = cv_gap_score_policy
        self._difficulty_score_policy = difficulty_score_policy
        self._diversity_score_policy = diversity_score_policy
        self._fatigue_score_policy = fatigue_score_policy

    def compute_level_score(
        self,
        *,
        question: Question,
        context: ScoringContext,
    ) -> float:
        return self._level_score_policy.compute(
            question=question,
            context=context,
        )

    def compute_market_score(
        self,
        *,
        question: Question,
        context: ScoringContext,
    ) -> float:
        return self._market_score_policy.compute(
            question=question,
            context=context,
        )

    def compute_cv_gap_score(
        self,
        *,
        question: Question,
        context: ScoringContext,
    ) -> float:
        return self._cv_gap_score_policy.compute(
            question=question,
            context=context,
        )

    def compute_difficulty_score(
        self,
        *,
        question: Question,
        context: ScoringContext,
    ) -> float:
        return self._difficulty_score_policy.compute(
            question=question,
            context=context,
        )

    def compute_diversity_score(
        self,
        *,
        question: Question,
        context: ScoringContext,
    ) -> float:
        return self._diversity_score_policy.compute(
            question=question,
            context=context,
        )

    def compute_fatigue_score(
        self,
        *,
        question: Question,
        context: ScoringContext,
    ) -> float:
        return self._fatigue_score_policy.compute(
            question=question,
            context=context,
        )