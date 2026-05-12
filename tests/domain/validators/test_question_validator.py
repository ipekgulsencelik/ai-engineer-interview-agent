import pytest

from src.domain.entities.question import Question
from src.domain.enums.level import Level
from src.domain.enums.question_category import QuestionCategory
from src.domain.enums.question_type import QuestionType
from src.domain.validators.question_validator import QuestionValidator


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
        ],
        "keywords": [
            "rag",
        ],
        "market_weight": 0.5,
        "followup_allowed": True,
    }

    payload.update(overrides)

    return Question(**payload)


# ---------------------------------------------------------
# MODEL TYPE VALIDATION
# ---------------------------------------------------------


def test_validator_rejects_non_question_instance() -> None:
    with pytest.raises(
        TypeError,
        match="question must be a Question instance",
    ):
        QuestionValidator.validate(object())


# ---------------------------------------------------------
# FIELD TYPE VALIDATION
# ---------------------------------------------------------


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        ("id", 123),
        ("text", []),
        ("category", "rag"),
        ("level", "JR"),
        ("difficulty", "hard"),
        ("question_type", "conceptual"),
        ("expected_points", "retrieval"),
        ("keywords", "rag"),
        ("market_weight", "0.5"),
        ("followup_allowed", "yes"),
    ],
)
def test_invalid_field_types_raise_error(
    field_name: str,
    value,
) -> None:
    with pytest.raises(TypeError):
        build_valid_question(
            **{
                field_name: value,
            }
        )


# ---------------------------------------------------------
# BOOL EDGE CASE
# ---------------------------------------------------------


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        ("difficulty", True),
        ("market_weight", False),
    ],
)
def test_bool_values_are_rejected_for_numeric_fields(
    field_name: str,
    value: bool,
) -> None:
    with pytest.raises(TypeError):
        build_valid_question(
            **{
                field_name: value,
            }
        )


def test_bool_field_accepts_bool_value() -> None:
    question = build_valid_question(
        followup_allowed=False,
    )

    assert question.followup_allowed is False


# ---------------------------------------------------------
# FINITE VALIDATION
# ---------------------------------------------------------


@pytest.mark.parametrize(
    "value",
    [
        float("inf"),
        float("-inf"),
        float("nan"),
    ],
)
def test_non_finite_market_weight_values_raise_error(
    value: float,
) -> None:
    with pytest.raises(
        ValueError,
        match="market_weight must be finite",
    ):
        build_valid_question(
            market_weight=value,
        )


# ---------------------------------------------------------
# LIST VALIDATION
# ---------------------------------------------------------


def test_expected_points_must_be_list() -> None:
    with pytest.raises(TypeError):
        build_valid_question(
            expected_points="retrieval",
        )


def test_keywords_must_be_list() -> None:
    with pytest.raises(TypeError):
        build_valid_question(
            keywords="rag",
        )


def test_expected_points_must_contain_only_strings() -> None:
    with pytest.raises(
        TypeError,
        match="All items in expected_points must be",
    ):
        build_valid_question(
            expected_points=[
                "valid",
                123,
            ],
        )


def test_keywords_must_contain_only_strings() -> None:
    with pytest.raises(
        TypeError,
        match="All items in keywords must be",
    ):
        build_valid_question(
            keywords=[
                "rag",
                object(),
            ],
        )


def test_expected_points_cannot_contain_empty_strings() -> None:
    with pytest.raises(
        ValueError,
        match="Items in expected_points cannot be empty",
    ):
        build_valid_question(
            expected_points=[
                "retrieval",
                "   ",
            ],
        )


def test_keywords_cannot_contain_empty_strings() -> None:
    with pytest.raises(
        ValueError,
        match="Items in keywords cannot be empty",
    ):
        build_valid_question(
            keywords=[
                "rag",
                "",
            ],
        )


# ---------------------------------------------------------
# BOUNDARY VALIDATION
# ---------------------------------------------------------


@pytest.mark.parametrize(
    "difficulty",
    [
        1,
        2,
        3,
    ],
)
def test_valid_difficulty_boundaries_are_accepted(
    difficulty: int,
) -> None:
    question = build_valid_question(
        difficulty=difficulty,
    )

    assert question.difficulty == difficulty


@pytest.mark.parametrize(
    "market_weight",
    [
        0.0,
        0.5,
        1.0,
    ],
)
def test_valid_market_weight_boundaries_are_accepted(
    market_weight: float,
) -> None:
    question = build_valid_question(
        market_weight=market_weight,
    )

    assert question.market_weight == market_weight