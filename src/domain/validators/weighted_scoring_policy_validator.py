from __future__ import annotations

from src.domain.scoring.final_score_calculator import (
    FinalScoreCalculator,
)
from src.domain.policies.cv_gap_score_policy import (
    CvGapScorePolicy,
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
from src.domain.policies.level_score_policy import (
    LevelScorePolicy,
)
from src.domain.policies.market_score_policy import (
    MarketScorePolicy,
)


class WeightedScoringPolicyValidator:
    """
    WeightedScoringPolicy dependency validation rules.
    """

    @staticmethod
    def validate_dependencies(
        *,
        level_score_policy: LevelScorePolicy,
        market_score_policy: MarketScorePolicy,
        cv_gap_score_policy: CvGapScorePolicy,
        difficulty_score_policy: DifficultyScorePolicy,
        diversity_score_policy: DiversityScorePolicy,
        fatigue_score_policy: FatigueScorePolicy,
        final_score_calculator: FinalScoreCalculator,
    ) -> None:
        if not isinstance(level_score_policy, LevelScorePolicy):
            raise TypeError("level_score_policy must be LevelScorePolicy.")

        if not isinstance(market_score_policy, MarketScorePolicy):
            raise TypeError("market_score_policy must be MarketScorePolicy.")

        if not isinstance(cv_gap_score_policy, CvGapScorePolicy):
            raise TypeError("cv_gap_score_policy must be CvGapScorePolicy.")

        if not isinstance(difficulty_score_policy, DifficultyScorePolicy):
            raise TypeError(
                "difficulty_score_policy must be DifficultyScorePolicy."
            )

        if not isinstance(diversity_score_policy, DiversityScorePolicy):
            raise TypeError(
                "diversity_score_policy must be DiversityScorePolicy."
            )

        if not isinstance(fatigue_score_policy, FatigueScorePolicy):
            raise TypeError("fatigue_score_policy must be FatigueScorePolicy.")

        if not isinstance(final_score_calculator, FinalScoreCalculator):
            raise TypeError(
                "final_score_calculator must be FinalScoreCalculator."
            )