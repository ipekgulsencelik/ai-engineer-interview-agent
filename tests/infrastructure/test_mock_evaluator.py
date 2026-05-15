import pytest

from src.domain.entities.question import Question
from src.infrastructure.evaluator.mock_evaluator import MockEvaluator


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


def test_mock_evaluator_returns_score() -> None:
    evaluator = MockEvaluator()

    result = evaluator.evaluate(
        make_question(), "RAG combines retrieval and generation."
    )

    assert result.score == 7
    assert result.feedback == "Mock evaluation completed successfully."


def test_mock_evaluator_empty_answer_raises_error() -> None:
    evaluator = MockEvaluator()

    with pytest.raises(ValueError, match="Answer cannot be empty"):
        evaluator.evaluate(make_question(), "")
