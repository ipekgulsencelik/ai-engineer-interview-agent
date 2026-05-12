import pytest

from src.domain.entities.question import Question
from src.domain.enums.level import Level
from src.domain.enums.question_category import QuestionCategory
from src.domain.enums.question_type import QuestionType
from src.domain.factories.question_factory import QuestionFactory


def test_factory_creates_question_successfully() -> None:
    question = QuestionFactory.create(
        id="rag_jr_001",
        text="What is RAG?",
        category="RAG",
        level="JR",
        difficulty=1,
        question_type="conceptual",
    )

    assert isinstance(question, Question)
    assert question.id == "rag_jr_001"
    assert question.text == "What is RAG?"
    assert question.category == QuestionCategory.RAG
    assert question.level == Level.JR
    assert question.question_type == QuestionType.CONCEPTUAL


def test_factory_normalizes_string_fields() -> None:
    question = QuestionFactory.create(
        id="  rag_jr_001  ",
        text="  What is RAG?  ",
        category="  RAG  ",
        level=" jr ",
        difficulty=1,
        question_type=" conceptual ",
    )

    assert question.id == "rag_jr_001"
    assert question.text == "What is RAG?"
    assert question.category == QuestionCategory.RAG
    assert question.level == Level.JR
    assert question.question_type == QuestionType.CONCEPTUAL


def test_factory_normalizes_category_values() -> None:
    question = QuestionFactory.create(
        id="q1",
        text="What is vector search?",
        category="Vector DB   &   Embedding",
        level="JR",
        difficulty=1,
        question_type="conceptual",
    )

    assert question.category == QuestionCategory.VECTOR_DB_AND_EMBEDDING


def test_factory_converts_none_lists_to_empty_lists() -> None:
    question = QuestionFactory.create(
        id="q1",
        text="What is RAG?",
        category="RAG",
        level="JR",
        difficulty=1,
        question_type="conceptual",
        expected_points=None,
        keywords=None,
    )

    assert question.expected_points == []
    assert question.keywords == []


def test_factory_strips_list_items() -> None:
    question = QuestionFactory.create(
        id="q1",
        text="What is RAG?",
        category="RAG",
        level="JR",
        difficulty=1,
        question_type="conceptual",
        expected_points=[
            " retrieval ",
            " generation ",
        ],
        keywords=[
            " rag ",
            " vector ",
        ],
    )

    assert question.expected_points == [
        "retrieval",
        "generation",
    ]

    assert question.keywords == [
        "rag",
        "vector",
    ]


def test_factory_invalid_level_raises_error() -> None:
    with pytest.raises(ValueError, match="Invalid level"):
        QuestionFactory.create(
            id="q1",
            text="What is RAG?",
            category="RAG",
            level="BEGINNER",
            difficulty=1,
            question_type="conceptual",
        )


def test_factory_invalid_question_type_raises_error() -> None:
    with pytest.raises(ValueError, match="Invalid question_type"):
        QuestionFactory.create(
            id="q1",
            text="What is RAG?",
            category="RAG",
            level="JR",
            difficulty=1,
            question_type="essay",
        )


def test_factory_invalid_category_raises_error() -> None:
    with pytest.raises(ValueError, match="Invalid category"):
        QuestionFactory.create(
            id="q1",
            text="What is RAG?",
            category="Mobile Development",
            level="JR",
            difficulty=1,
            question_type="conceptual",
        )