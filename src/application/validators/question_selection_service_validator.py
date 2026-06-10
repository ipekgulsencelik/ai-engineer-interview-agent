from __future__ import annotations

from src.domain.entities.question import Question
from src.domain.scoring.scoring_context import ScoringContext


class QuestionSelectionServiceValidator:
    """
    QuestionSelectionService input validation helper'ı.
    """

    @staticmethod
    def validate_select_inputs(
        *,
        questions: list[Question],
        context: ScoringContext,
    ) -> None:
        if not isinstance(questions, list):
            raise TypeError("questions must be a list.")

        if not questions:
            raise ValueError("questions cannot be empty.")

        for question in questions:
            if not isinstance(question, Question):
                raise TypeError("questions must contain Question instances.")

        if not isinstance(context, ScoringContext):
            raise TypeError("context must be a ScoringContext.")