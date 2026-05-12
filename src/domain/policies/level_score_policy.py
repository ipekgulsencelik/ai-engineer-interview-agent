from __future__ import annotations

from src.domain.constants.scoring import (
    EXACT_LEVEL_MATCH_SCORE,
    LEVEL_RANKS,
    ONE_LEVEL_DISTANCE_SCORE,
    TWO_LEVEL_DISTANCE_SCORE,
)
from src.domain.entities.question import Question
from src.domain.enums.level import Level
from src.domain.validators.scoring_policy_input_validator import (
    ScoringPolicyInputValidator,
)
from src.domain.scoring.scoring_context import (
    ScoringContext,
)


class LevelScorePolicy:
    """
    Question level ile current interview level uyumunu hesaplar.
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

        level_distance = self._compute_level_distance(
            question_level=question.level,
            current_level=context.current_level,
        )

        return self._resolve_score_by_distance(
            level_distance,
        )

    @staticmethod
    def _compute_level_distance(
        *,
        question_level: Level,
        current_level: Level,
    ) -> int:
        return abs(
            LEVEL_RANKS[question_level]
            - LEVEL_RANKS[current_level]
        )

    @staticmethod
    def _resolve_score_by_distance(
        level_distance: int,
    ) -> float:
        if level_distance == 0:
            return EXACT_LEVEL_MATCH_SCORE

        if level_distance == 1:
            return ONE_LEVEL_DISTANCE_SCORE

        return TWO_LEVEL_DISTANCE_SCORE