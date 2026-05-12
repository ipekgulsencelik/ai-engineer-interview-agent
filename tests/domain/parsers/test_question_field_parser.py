import pytest

from src.domain.enums.level import Level
from src.domain.enums.question_category import QuestionCategory
from src.domain.enums.question_type import QuestionType
from src.domain.parsers.question_field_parser import QuestionFieldParser


@pytest.mark.parametrize(
    ("raw_value", "expected"),
    [
        ("JR", Level.JR),
        ("jr", Level.JR),
        (" Jr ", Level.JR),
        (Level.JR, Level.JR),
    ],
)
def test_parse_level_returns_expected_enum(
    raw_value,
    expected,
) -> None:
    assert QuestionFieldParser.parse_level(raw_value) == expected


def test_parse_level_with_invalid_value_raises_error() -> None:
    with pytest.raises(ValueError, match="Invalid level"):
        QuestionFieldParser.parse_level("BEGINNER")


def test_parse_level_with_invalid_type_raises_error() -> None:
    with pytest.raises(TypeError, match="level must be a string or Level"):
        QuestionFieldParser.parse_level(123)


@pytest.mark.parametrize(
    ("raw_value", "expected"),
    [
        ("conceptual", QuestionType.CONCEPTUAL),
        (" Conceptual ", QuestionType.CONCEPTUAL),
        ("coding", QuestionType.CODING),
        ("scenario", QuestionType.SCENARIO),
        (QuestionType.CODING, QuestionType.CODING),
    ],
)
def test_parse_question_type_returns_expected_enum(
    raw_value,
    expected,
) -> None:
    assert QuestionFieldParser.parse_question_type(raw_value) == expected


def test_parse_question_type_with_invalid_value_raises_error() -> None:
    with pytest.raises(ValueError, match="Invalid question_type"):
        QuestionFieldParser.parse_question_type("essay")


def test_parse_question_type_with_invalid_type_raises_error() -> None:
    with pytest.raises(
        TypeError,
        match="question_type must be a string or QuestionType",
    ):
        QuestionFieldParser.parse_question_type([])


@pytest.mark.parametrize(
    ("raw_value", "expected"),
    [
        ("rag", QuestionCategory.RAG),
        ("RAG", QuestionCategory.RAG),
        ("  RAG  ", QuestionCategory.RAG),
        (
            "Vector DB & Embedding",
            QuestionCategory.VECTOR_DB_AND_EMBEDDING,
        ),
        (
            "Vector DB   &   Embedding",
            QuestionCategory.VECTOR_DB_AND_EMBEDDING,
        ),
        (
            "Prompt Engineering",
            QuestionCategory.PROMPT_ENGINEERING,
        ),
        (
            "Fine-tuning",
            QuestionCategory.FINE_TUNING,
        ),
        (
            QuestionCategory.AGENTS,
            QuestionCategory.AGENTS,
        ),
    ],
)
def test_parse_category_returns_expected_enum(
    raw_value,
    expected,
) -> None:
    assert QuestionFieldParser.parse_category(raw_value) == expected


def test_parse_category_with_invalid_value_raises_error() -> None:
    with pytest.raises(ValueError, match="Invalid category"):
        QuestionFieldParser.parse_category("Mobile Development")


def test_parse_category_with_invalid_type_raises_error() -> None:
    with pytest.raises(
        TypeError,
        match="category must be a string or QuestionCategory",
    ):
        QuestionFieldParser.parse_category({})