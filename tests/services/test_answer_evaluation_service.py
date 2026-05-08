from src.domain.question.question import Question
from src.infrastructure.evaluator.mock_evaluator import MockEvaluator
from src.services.answer_evaluation_service import AnswerEvaluationService


def make_question() -> Question:
    return Question(
        id="q1",
        text="What is RAG?",
        category="RAG",
        level="JR",
        difficulty=1,
        question_type="conceptual",
        expected_points=[],
        keywords=[],
    )


def test_answer_evaluation_service_returns_evaluation_result() -> None:
    service = AnswerEvaluationService(evaluator=MockEvaluator())

    result = service.evaluate_answer(
        question=make_question(),
        answer="RAG combines retrieval and generation.",
    )

    assert result.success is True
    assert result.data is not None
    assert result.data.score == 7
    assert result.data.feedback == "Mock evaluation completed successfully."


def test_answer_evaluation_service_empty_answer_returns_failure() -> None:
    service = AnswerEvaluationService(evaluator=MockEvaluator())

    result = service.evaluate_answer(
        question=make_question(),
        answer="",
    )

    assert result.success is False
    assert result.error == "Answer cannot be empty."
