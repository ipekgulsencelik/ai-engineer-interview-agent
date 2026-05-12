from __future__ import annotations

from src.domain.entities.question import Question
from src.domain.scoring.scoring_context import ScoringContext


class ScoringPolicyInputValidator:
    """
    Stateless scoring policy input validation utility.
    """

    @staticmethod
    def validate(
        *,
        question: Question,
        context: ScoringContext,
    ) -> None:
        if not isinstance(question, Question):
            raise TypeError(
                "question must be a Question instance."
            )

        if not isinstance(context, ScoringContext):
            raise TypeError(
                "context must be a ScoringContext instance."
            )