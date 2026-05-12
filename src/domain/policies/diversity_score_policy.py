from __future__ import annotations

from src.domain.constants.scoring import (
    ASKED_QUESTION_DIVERSITY_SCORE,
    UNASKED_QUESTION_DIVERSITY_SCORE,
)
from src.domain.entities.question import Question
from src.domain.validators.scoring_policy_input_validator import (
    ScoringPolicyInputValidator,
)
from src.domain.scoring.scoring_context import (
    ScoringContext,
)


class DiversityScorePolicy:
    """
    Daha önce sorulmuş question tekrarını azaltan diversity policy.
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
        
        if self._is_question_already_asked(
            question=question,
            context=context,
        ):
            return ASKED_QUESTION_DIVERSITY_SCORE

        return UNASKED_QUESTION_DIVERSITY_SCORE

    @staticmethod
    def _is_question_already_asked(
        *,
        question: Question,
        context: ScoringContext,
    ) -> bool:
        return question.id in context.asked_question_ids