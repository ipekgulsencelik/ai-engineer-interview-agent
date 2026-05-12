from __future__ import annotations

import pytest

from src.application.ports.evaluator import Evaluator
from src.application.validators.answer_evaluation_service_validator import (
    AnswerEvaluationServiceValidator,
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
    def evaluate(
        self,
        *,
        question: Question,
        answer: str,
    ) -> EvaluationResult:
        return EvaluationResult(
            score=8.0,
            feedback="Good answer.",
        )


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
    )


def test_validate_evaluator_accepts_evaluator() -> None:
    evaluator = FakeEvaluator()

    AnswerEvaluationServiceValidator.validate_evaluator(
        evaluator,
    )


def test_validate_evaluator_rejects_invalid_evaluator() -> None:
    with pytest.raises(TypeError):
        AnswerEvaluationServiceValidator.validate_evaluator(
            object(),  # type: ignore[arg-type]
        )


def test_validate_evaluation_input_returns_normalized_answer() -> None:
    question = build_question()

    normalized_answer = (
        AnswerEvaluationServiceValidator.validate_evaluation_input(
            question=question,
            answer="   Valid answer.   ",
        )
    )

    assert normalized_answer == "Valid answer."


def test_validate_question_accepts_question() -> None:
    question = build_question()

    AnswerEvaluationServiceValidator.validate_question(
        question,
    )


def test_validate_question_rejects_invalid_question() -> None:
    with pytest.raises(TypeError):
        AnswerEvaluationServiceValidator.validate_question(
            object(),  # type: ignore[arg-type]
        )


@pytest.mark.parametrize(
    "answer",
    [
        "",
        "   ",
    ],
)
def test_validate_answer_rejects_empty_answer(
    answer: str,
) -> None:
    with pytest.raises(ValueError):
        AnswerEvaluationServiceValidator.validate_answer(
            answer,
        )


def test_validate_answer_rejects_non_string_answer() -> None:
    with pytest.raises(TypeError):
        AnswerEvaluationServiceValidator.validate_answer(
            123,  # type: ignore[arg-type]
        )


def test_validate_answer_returns_stripped_answer() -> None:
    normalized_answer = AnswerEvaluationServiceValidator.validate_answer(
        "   Clean answer.   ",
    )

    assert normalized_answer == "Clean answer."


def test_validate_result_accepts_evaluation_result() -> None:
    result = build_result()

    AnswerEvaluationServiceValidator.validate_result(
        result,
    )


def test_validate_result_rejects_invalid_result() -> None:
    with pytest.raises(RuntimeError):
        AnswerEvaluationServiceValidator.validate_result(
            object(),  # type: ignore[arg-type]
        )