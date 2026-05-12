from __future__ import annotations

from src.domain.evaluation.evaluator import Evaluator
from src.domain.entities.question import Question
from src.domain.results.evaluation_result import EvaluationResult


class AnswerEvaluationServiceValidator:
    @staticmethod
    def validate_evaluator(
        evaluator: Evaluator,
    ) -> None:
        if not isinstance(evaluator, Evaluator):
            raise TypeError(
                "evaluator must implement Evaluator interface."
            )

    @classmethod
    def validate_evaluation_input(
        cls,
        *,
        question: Question,
        answer: str,
    ) -> str:
        cls.validate_question(
            question,
        )

        return cls.validate_answer(
            answer,
        )

    @staticmethod
    def validate_question(
        question: Question,
    ) -> None:
        if not isinstance(question, Question):
            raise TypeError(
                "question must be a Question instance."
            )

    @staticmethod
    def validate_answer(
        answer: str,
    ) -> str:
        if not isinstance(answer, str):
            raise TypeError(
                "answer must be a string."
            )

        normalized = answer.strip()

        if not normalized:
            raise ValueError(
                "answer cannot be empty."
            )

        return normalized

    @staticmethod
    def validate_result(
        result: EvaluationResult,
    ) -> None:
        if not isinstance(result, EvaluationResult):
            raise RuntimeError(
                "evaluator must return an "
                "EvaluationResult instance."
            )
