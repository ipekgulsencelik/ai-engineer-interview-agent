from __future__ import annotations

from src.application.ports.scoring_engine import (
    ScoringEngine,
)
from src.domain.entities.question import Question
from src.domain.scoring.scoring_context import (
    ScoringContext,
)


class CandidateQuestionRankerValidator:
    """
    CandidateQuestionRanker validation rules.
    """

    @staticmethod
    def validate_scoring_engine(
        scoring_engine: ScoringEngine,
    ) -> None:
        if not isinstance(scoring_engine, ScoringEngine):
            raise TypeError(
                "scoring_engine must implement "
                "ScoringEngine."
            )

    @staticmethod
    def validate_questions(
        questions: list[Question],
    ) -> None:
        if not isinstance(questions, list):
            raise TypeError(
                "questions must be a list."
            )

        for index, question in enumerate(
            questions,
        ):
            if not isinstance(question, Question):
                raise TypeError(
                    "All questions must be Question instances. "
                    f"Invalid index: {index}."
                )

    @staticmethod
    def validate_context(
        context: ScoringContext,
    ) -> None:
        if not isinstance(context, ScoringContext):
            raise TypeError(
                "context must be a "
                "ScoringContext instance."
            )