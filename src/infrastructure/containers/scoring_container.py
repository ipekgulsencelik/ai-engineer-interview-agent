from __future__ import annotations

from functools import cached_property

from src.domain.policies.cv_gap_score_policy import CvGapScorePolicy
from src.domain.policies.difficulty_score_policy import DifficultyScorePolicy
from src.domain.policies.diversity_score_policy import DiversityScorePolicy
from src.domain.policies.fatigue_score_policy import FatigueScorePolicy
from src.domain.policies.level_score_policy import LevelScorePolicy
from src.domain.policies.market_score_policy import MarketScorePolicy
from src.domain.policies.weighted_scoring_policy import WeightedScoringPolicy
from src.domain.scoring.final_score_calculator import FinalScoreCalculator
from src.domain.scoring.weighted_scoring_engine import WeightedScoringEngine


class ScoringContainer:
    """
    Scoring dependency container.
    """

    @cached_property
    def scoring_policy(
        self,
    ) -> WeightedScoringPolicy:
        return WeightedScoringPolicy(
            level_score_policy=LevelScorePolicy(),
            market_score_policy=MarketScorePolicy(),
            cv_gap_score_policy=CvGapScorePolicy(),
            difficulty_score_policy=DifficultyScorePolicy(),
            diversity_score_policy=DiversityScorePolicy(),
            fatigue_score_policy=FatigueScorePolicy(),
            final_score_calculator=FinalScoreCalculator(),
        )

    @cached_property
    def scoring_engine(
        self,
    ) -> WeightedScoringEngine:
        return WeightedScoringEngine(
            policy=self.scoring_policy,
        )