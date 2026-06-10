from __future__ import annotations

from src.domain.constants.fatigue_scoring import (
    HIGH_DIFFICULTY_FATIGUE_PENALTY_STEP,
    HIGH_DIFFICULTY_THRESHOLD,
    REPEATED_CATEGORY_FATIGUE_PENALTY_STEP,
    REPEATED_QUESTION_TYPE_FATIGUE_PENALTY_STEP,
)
from src.domain.entities.question import Question
from src.domain.value_objects.question_fatigue import (
    QuestionFatigue,
)


class FatiguePenaltyPolicy:
    """
    Fatigue penalty calculation policy.
    """

    @staticmethod
    def calculate(
        *,
        question: Question,
        fatigue: QuestionFatigue,
    ) -> float:
        penalty = (
            fatigue.repeated_category_count
            * REPEATED_CATEGORY_FATIGUE_PENALTY_STEP
        )

        penalty += (
            fatigue.repeated_question_type_count
            * REPEATED_QUESTION_TYPE_FATIGUE_PENALTY_STEP
        )

        if question.difficulty >= HIGH_DIFFICULTY_THRESHOLD:
            penalty += (
                fatigue.recent_high_difficulty_count
                * HIGH_DIFFICULTY_FATIGUE_PENALTY_STEP
            )

        return penalty