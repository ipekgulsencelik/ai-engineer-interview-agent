from __future__ import annotations

from src.domain.constants.scoring import (
    DEFAULT_FATIGUE_SCORE,
    HIGH_PERFORMANCE_THRESHOLD,
    LOW_PERFORMANCE_THRESHOLD,
    MAX_SCORE,
    MIN_SCORE,
)
from src.domain.entities.question import Question
from src.domain.enums.difficulty import Difficulty
from src.domain.validators.scoring_policy_input_validator import (
    ScoringPolicyInputValidator,
)
from src.domain.scoring.scoring_context import (
    ScoringContext,
)


class FatigueScorePolicy:
    """
    Candidate fatigue-aware scoring policy.
    """

    def compute(
        self,
        *,
        question: Question,
        context: ScoringContext,
    ) -> float:
        ScoringPolicyInputValidator.validate(
            question=question,
            context=context,
        )
        
        if not context.recent_scores:
            return DEFAULT_FATIGUE_SCORE

        average_recent_score = self._compute_average_score(
            context.recent_scores,
        )

        return self._resolve_fatigue_score(
            average_recent_score=average_recent_score,
            difficulty=question.difficulty,
        )

    @staticmethod
    def _compute_average_score(
        scores: list[float],
    ) -> float:
        return sum(scores) / len(scores)

    @staticmethod
    def _resolve_fatigue_score(
        *,
        average_recent_score: float,
        difficulty: Difficulty,
    ) -> float:
        if average_recent_score <= LOW_PERFORMANCE_THRESHOLD:
            return FatigueScorePolicy._resolve_low_performance_score(
                difficulty,
            )

        if average_recent_score >= HIGH_PERFORMANCE_THRESHOLD:
            return FatigueScorePolicy._resolve_high_performance_score(
                difficulty,
            )

        return DEFAULT_FATIGUE_SCORE

    @staticmethod
    def _resolve_low_performance_score(
        difficulty: Difficulty,
    ) -> float:
        if difficulty == Difficulty.HARD:
            return MIN_SCORE

        return DEFAULT_FATIGUE_SCORE

    @staticmethod
    def _resolve_high_performance_score(
        difficulty: Difficulty,
    ) -> float:
        if difficulty == Difficulty.HARD:
            return MAX_SCORE

        return DEFAULT_FATIGUE_SCORE