import pytest

from src.domain.entities.question import Question
from src.domain.enums.level import Level
from src.domain.enums.question_category import QuestionCategory
from src.domain.enums.question_type import QuestionType


def build_valid_question(**overrides) -> Question:
    payload = {
        "id": "rag_jr_001",
        "text": "What is RAG?",
        "category": QuestionCategory.RAG,
        "level": Level.JR,
        "difficulty": 1,
        "question_type": QuestionType.CONCEPTUAL,
        "expected_points": [
            "retrieval",
            "generation",
        ],
        "keywords": [
            "rag",
            "retrieval",
        ],
        "market_weight": 0.5,
        "followup_allowed": True,
    }

    payload.update(overrides)

    return Question(**payload)


def test_question_can_be_created_with_valid_domain_safe_data() -> None:
    question = build_valid_question()

    assert question.id == "rag_jr_001"
    assert question.text == "What is RAG?"
    assert question.category == QuestionCategory.RAG
    assert question.level == Level.JR
    assert question.difficulty == 1
    assert question.question_type == QuestionType.CONCEPTUAL
    assert question.expected_points == [
        "retrieval",
        "generation",
    ]
    assert question.keywords == [
        "rag",
        "retrieval",
    ]
    assert question.market_weight == 0.5
    assert question.followup_allowed is True


def test_question_uses_default_collection_values() -> None:
    question = Question(
        id="rag_jr_001",
        text="What is RAG?",
        category=QuestionCategory.RAG,
        level=Level.JR,
        difficulty=1,
        question_type=QuestionType.CONCEPTUAL,
    )

    assert question.expected_points == []
    assert question.keywords == []


def test_question_is_immutable() -> None:
    question = build_valid_question()

    with pytest.raises(Exception):
        question.id = "changed"


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        ("id", ""),
        ("id", "   "),
        ("text", ""),
        ("text", "   "),
    ],
)
def test_question_required_string_fields_cannot_be_empty(
    field_name: str,
    value: str,
) -> None:
    with pytest.raises(
        ValueError,
        match=f"{field_name} cannot be empty",
    ):
        build_valid_question(
            **{
                field_name: value,
            }
        )


def test_question_difficulty_cannot_be_below_minimum() -> None:
    with pytest.raises(
        ValueError,
        match="difficulty must be greater than or equal to 1",
    ):
        build_valid_question(difficulty=0)


def test_question_difficulty_cannot_be_above_maximum() -> None:
    with pytest.raises(
        ValueError,
        match="difficulty must be less than or equal to 3",
    ):
        build_valid_question(difficulty=4)


def test_question_market_weight_cannot_be_below_minimum() -> None:
    with pytest.raises(
        ValueError,
        match="market_weight must be greater than or equal to 0.0",
    ):
        build_valid_question(market_weight=-0.1)


def test_question_market_weight_cannot_be_above_maximum() -> None:
    with pytest.raises(
        ValueError,
        match="market_weight must be less than or equal to 1.0",
    ):
        build_valid_question(market_weight=1.1)