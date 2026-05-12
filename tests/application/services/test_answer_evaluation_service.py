from __future__ import annotations

import pytest

from src.application.exceptions.answer_evaluation_error import (
    AnswerEvaluationError,
)
from src.application.ports.evaluator import Evaluator
from src.application.services.answer_evaluation_service import (
    AnswerEvaluationService,
)
from src.domain.entities.question import Question
from src.domain.enums.level import Level
from src.domain.enums.question_category import (
    QuestionCategory,
)
from src.domain.enums.question_type import (
    QuestionType,
)
from src.domain.results.evaluation_result import EvaluationResult


class FakeEvaluator(Evaluator):
    def __init__(
        self,
        result: EvaluationResult,
    ) -> None:
        self.result = result
        self.received_question: Question | None = None
        self.received_answer: str | None = None

    def evaluate(
        self,
        *,
        question: Question,
        answer: str,
    ) -> EvaluationResult:
        self.received_question = question
        self.received_answer = answer

        return self.result


class FailingEvaluator(Evaluator):
    def evaluate(
        self,
        *,
        question: Question,
        answer: str,
    ) -> EvaluationResult:
        raise ValueError("provider failed")


class InvalidResultEvaluator(Evaluator):
    def evaluate(
        self,
        *,
        question: Question,
        answer: str,
    ) -> EvaluationResult:
        return "invalid-result"  # type: ignore[return-value]


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
        score=8.0,
        feedback="Good answer.",
        technical_accuracy=8.0,
        depth=7.0,
        communication=9.0,
    )


def test_evaluate_returns_evaluation_result() -> None:
    question = build_question()
    expected_result = build_result()
    evaluator = FakeEvaluator(expected_result)
    service = AnswerEvaluationService(evaluator)

    result = service.evaluate(
        question=question,
        answer="RAG combines retrieval and generation.",
    )

    assert isinstance(result, EvaluationResult)
    assert result.score == expected_result.score
    assert result.feedback == expected_result.feedback


def test_evaluate_normalizes_answer_before_passing_to_evaluator() -> None:
    question = build_question()
    evaluator = FakeEvaluator(build_result())
    service = AnswerEvaluationService(evaluator)

    service.evaluate(
        question=question,
        answer="   normalized answer   ",
    )

    assert evaluator.received_answer == "normalized answer"


def test_evaluate_passes_question_to_evaluator() -> None:
    question = build_question()
    evaluator = FakeEvaluator(build_result())
    service = AnswerEvaluationService(evaluator)

    service.evaluate(
        question=question,
        answer="Valid answer.",
    )

    assert evaluator.received_question is question


def test_evaluate_adds_latency_to_result_metadata() -> None:
    question = build_question()
    evaluator = FakeEvaluator(build_result())
    service = AnswerEvaluationService(evaluator)

    result = service.evaluate(
        question=question,
        answer="Valid answer.",
    )

    assert result.metadata.latency_seconds is not None
    assert result.metadata.latency_seconds >= 0.0


@pytest.mark.parametrize(
    "answer",
    [
        "",
        "   ",
    ],
)
def test_evaluate_rejects_empty_answer(
    answer: str,
) -> None:
    question = build_question()
    evaluator = FakeEvaluator(build_result())
    service = AnswerEvaluationService(evaluator)

    with pytest.raises(ValueError):
        service.evaluate(
            question=question,
            answer=answer,
        )


def test_evaluate_rejects_non_string_answer() -> None:
    question = build_question()
    evaluator = FakeEvaluator(build_result())
    service = AnswerEvaluationService(evaluator)

    with pytest.raises(TypeError):
        service.evaluate(
            question=question,
            answer=123,  # type: ignore[arg-type]
        )


def test_constructor_rejects_invalid_evaluator() -> None:
    with pytest.raises(TypeError):
        AnswerEvaluationService(
            evaluator=object(),  # type: ignore[arg-type]
        )


def test_evaluate_wraps_evaluator_exception() -> None:
    question = build_question()
    service = AnswerEvaluationService(
        FailingEvaluator(),
    )

    with pytest.raises(
        AnswerEvaluationError,
        match="Failed to evaluate answer",
    ):
        service.evaluate(
            question=question,
            answer="Valid answer.",
        )


def test_evaluate_rejects_invalid_evaluator_result() -> None:
    question = build_question()
    service = AnswerEvaluationService(
        InvalidResultEvaluator(),
    )

    with pytest.raises(RuntimeError):
        service.evaluate(
            question=question,
            answer="Valid answer.",
        )