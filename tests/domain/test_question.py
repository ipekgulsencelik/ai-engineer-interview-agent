import pytest

from src.domain.question.question import Question


def test_question_can_be_created_with_valid_data() -> None:
    question = Question(
        id="rag_jr_001",
        text="What is RAG?",
        category="RAG",
        level="JR",
        difficulty=1,
        question_type="conceptual",
        expected_points=["retrieval", "generation"],
        keywords=["rag", "retrieval"],
    )

    assert question.id == "rag_jr_001"
    assert question.level == "JR"
    assert question.market_weight == 0.5
    assert question.followup_allowed is True


def test_question_empty_text_raises_error() -> None:
    with pytest.raises(ValueError, match="Question text cannot be empty"):
        Question(
            id="q1",
            text="",
            category="RAG",
            level="JR",
            difficulty=1,
            question_type="conceptual",
            expected_points=[],
            keywords=[],
        )


def test_question_invalid_level_raises_error() -> None:
    with pytest.raises(ValueError, match="Invalid question level"):
        Question(
            id="q1",
            text="What is RAG?",
            category="RAG",
            level="BEGINNER",
            difficulty=1,
            question_type="conceptual",
            expected_points=[],
            keywords=[],
        )


def test_question_invalid_difficulty_raises_error() -> None:
    with pytest.raises(ValueError, match="Question difficulty must be between 1 and 3"):
        Question(
            id="q1",
            text="What is RAG?",
            category="RAG",
            level="JR",
            difficulty=5,
            question_type="conceptual",
            expected_points=[],
            keywords=[],
        )


def test_question_invalid_market_weight_raises_error() -> None:
    with pytest.raises(ValueError, match="Market weight must be between 0 and 1"):
        Question(
            id="q1",
            text="What is RAG?",
            category="RAG",
            level="JR",
            difficulty=1,
            question_type="conceptual",
            expected_points=[],
            keywords=[],
            market_weight=1.5,
        )
