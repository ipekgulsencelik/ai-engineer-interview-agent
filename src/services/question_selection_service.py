from __future__ import annotations

from typing import Protocol

from src.domain.entities.question import Question
from src.domain.scoring.scoring_context import ScoringContext


class ScoringEngineLike(Protocol):
    def score(self, question: Question, context: ScoringContext) -> float: ...


class QuestionSelectionService:

    def __init__(self, scoring_engine: ScoringEngineLike) -> None:
        if scoring_engine is None:
            raise ValueError("scoring_engine is required.")
        self._scoring_engine = scoring_engine

    def select_question(
        self,
        questions: list[Question],
        context: ScoringContext,
    ) -> Question:

        if not isinstance(questions, list):
            raise TypeError("questions must be a list of Question.")

        if not isinstance(context, ScoringContext):
            raise TypeError("context must be a ScoringContext instance.")
        
        available_questions = [
            question
            for question in questions
            if question.id not in context.asked_question_ids
        ]

        if not available_questions:
            raise ValueError("No available questions to select.")

        return max(
            available_questions,
            key=lambda question: self._scoring_engine.score(
                question,
                context,
            ),
        )