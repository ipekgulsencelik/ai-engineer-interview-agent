from __future__ import annotations

import pytest

from src.application.exceptions.answer_evaluation_error import (
    AnswerEvaluationError,
)
from src.domain.evaluation.evaluator import Evaluator
from src.application.services.answer_evaluation_service import (
    AnswerEvaluationService,
)
from src.domain.entities.question import Question
from src.domain.enums.level import Level
from src.domain.enums.question_category import QuestionCategory
from src.domain.enums.question_type import QuestionType
from src.domain.results.evaluation_result import EvaluationResult


class StubEvaluator(Evaluator):
    def __init__(self, result: EvaluationResult) -> None:
        self._result = result

    def evaluate(self, *, question: Question, answer: str) -> EvaluationResult:
        return self._result


class ExplodingEvaluator(Evaluator):
    def evaluate(self, *, question: Question, answer: str) -> EvaluationResult:
        raise RuntimeError("boom")


def build_question() -> Question:
    return Question(
        id="q1",
        text="What is RAG?",
        category=QuestionCategory.RAG,
        level=Level.JR,
        difficulty=1,
        question_type=QuestionType.CONCEPTUAL,
        expected_points=[],
        keywords=[],
    )


def build_result() -> EvaluationResult:
    return EvaluationResult(
        score=7.0,
        feedback="Good fundamentals.",
        technical_accuracy=7.0,
        depth=7.0,
        communication=7.0,
    )


def test_evaluate_returns_successful_result() -> None:
    service = AnswerEvaluationService(
        evaluator=StubEvaluator(build_result()),
    )

    result = service.evaluate(
        question=build_question(),
        answer="RAG combines retrieval and generation.",
    )

    assert result.score == 7.0
    assert result.feedback == "Good fundamentals."


def test_evaluate_rejects_empty_answer() -> None:
    service = AnswerEvaluationService(
        evaluator=StubEvaluator(build_result()),
    )

    with pytest.raises(ValueError):
        service.evaluate(
            question=build_question(),
            answer="   ",
        )


def test_evaluate_wraps_provider_failures() -> None:
    service = AnswerEvaluationService(
        evaluator=ExplodingEvaluator(),
    )

    with pytest.raises(AnswerEvaluationError):
        service.evaluate(
            question=build_question(),
            answer="Valid answer",
        )
