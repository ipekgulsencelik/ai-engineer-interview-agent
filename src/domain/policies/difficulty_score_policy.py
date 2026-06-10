from __future__ import annotations

from src.domain.constants.scoring import (
    DEFAULT_DIFFICULTY_SCORE,
    HIGH_PERFORMANCE_DIFFICULTY_SCORES,
    HIGH_PERFORMANCE_THRESHOLD,
    LOW_PERFORMANCE_DIFFICULTY_SCORES,
    LOW_PERFORMANCE_THRESHOLD,
    MID_PERFORMANCE_DIFFICULTY_SCORES,
)
from src.domain.entities.question import Question
from src.domain.enums.difficulty import Difficulty
from src.domain.validators.scoring_policy_input_validator import (
    ScoringPolicyInputValidator,
)
from src.domain.scoring.scoring_context import (
    ScoringContext,
)


class DifficultyScorePolicy:
    """
    Candidate performance'a göre question difficulty uyumunu hesaplar.
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

        performance_bucket = self._resolve_performance_bucket(
            context.recent_scores,
        )

        difficulty_scores = self._resolve_score_map(
            performance_bucket,
        )

        return difficulty_scores.get(
            question.difficulty,
            DEFAULT_DIFFICULTY_SCORE,
        )

    @staticmethod
    def _resolve_performance_bucket(
        recent_scores: list[float],
    ) -> str:
        if not recent_scores:
            return "mid"

        average_score = sum(recent_scores) / len(
            recent_scores,
        )

        if average_score >= HIGH_PERFORMANCE_THRESHOLD:
            return "high"

        if average_score <= LOW_PERFORMANCE_THRESHOLD:
            return "low"

        return "mid"

    @staticmethod
    def _resolve_score_map(
        performance_bucket: str,
    ) -> dict[Difficulty, float]:
        if performance_bucket == "high":
            return HIGH_PERFORMANCE_DIFFICULTY_SCORES

        if performance_bucket == "low":
            return LOW_PERFORMANCE_DIFFICULTY_SCORES

        return MID_PERFORMANCE_DIFFICULTY_SCORES