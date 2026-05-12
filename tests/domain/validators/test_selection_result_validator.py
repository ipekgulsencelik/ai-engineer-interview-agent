from datetime import datetime, timezone

import pytest

from src.domain.entities.question import Question
from src.domain.enums.level import Level
from src.domain.enums.question_category import QuestionCategory
from src.domain.enums.question_type import QuestionType
from src.domain.results.selection_breakdown import SelectionBreakdown
from src.domain.results.selection_result import SelectionResult
from src.domain.validators.selection_result_validator import (
    SelectionResultValidator,
)


def build_question(**overrides) -> Question:
    payload = {
        "id": "rag_jr_001",
        "text": "What is RAG?",
        "category": QuestionCategory.RAG,
        "level": Level.JR,
        "difficulty": 1,
        "question_type": QuestionType.CONCEPTUAL,
        "expected_points": ["retrieval"],
        "keywords": ["rag"],
        "market_weight": 0.9,
        "followup_allowed": True,
    }

    payload.update(overrides)

    return Question(**payload)


def build_breakdown(**overrides) -> SelectionBreakdown:
    payload = {
        "level_score": 0.8,
        "market_score": 0.9,
        "cv_gap_score": 0.7,
        "difficulty_score": 0.6,
        "diversity_score": 0.5,
        "fatigue_score": 1.0,
        "final_score": 0.82,
    }

    payload.update(overrides)

    return SelectionBreakdown(**payload)


def build_result(**overrides) -> SelectionResult:
    payload = {
        "question": build_question(),
        "final_score": 0.82,
        "breakdown": build_breakdown(),
        "selected_at": datetime.now(timezone.utc),
        "rank": 1,
        "candidate_count": 5,
    }

    payload.update(overrides)

    return SelectionResult(**payload)


def test_validator_accepts_valid_selection_result() -> None:
    result = build_result()

    SelectionResultValidator.validate(result)


def test_validator_rejects_non_selection_result_instance() -> None:
    with pytest.raises(
        TypeError,
        match="result must be a SelectionResult instance",
    ):
        SelectionResultValidator.validate(object())


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        ("question", object()),
        ("final_score", "0.82"),
        ("breakdown", object()),
        ("selected_at", "2026-01-01"),
        ("rank", "1"),
        ("candidate_count", "5"),
    ],
)
def test_validator_rejects_invalid_field_types(
    field_name: str,
    value,
) -> None:
    with pytest.raises(TypeError):
        build_result(
            **{
                field_name: value,
            }
        )


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        ("final_score", True),
        ("rank", False),
        ("candidate_count", True),
    ],
)
def test_validator_rejects_bool_values_for_numeric_fields(
    field_name: str,
    value: bool,
) -> None:
    with pytest.raises(TypeError):
        build_result(
            **{
                field_name: value,
            }
        )


@pytest.mark.parametrize(
    "value",
    [
        float("inf"),
        float("-inf"),
        float("nan"),
    ],
)
def test_validator_rejects_non_finite_final_score(
    value: float,
) -> None:
    with pytest.raises(
        ValueError,
        match="final_score must be finite",
    ):
        build_result(
            final_score=value,
        )


def test_validator_rejects_negative_final_score() -> None:
    with pytest.raises(
        ValueError,
        match="final_score must be greater than or equal to 0.0",
    ):
        build_result(
            final_score=-0.1,
        )


def test_validator_rejects_naive_selected_at_datetime() -> None:
    with pytest.raises(
        ValueError,
        match="selected_at must be timezone-aware",
    ):
        build_result(
            selected_at=datetime.now(),
        )


def test_validator_accepts_none_rank_and_candidate_count() -> None:
    result = build_result(
        rank=None,
        candidate_count=None,
    )

    SelectionResultValidator.validate(result)


def test_validator_rejects_rank_below_minimum() -> None:
    with pytest.raises(
        ValueError,
        match="rank must be greater than or equal to 1",
    ):
        build_result(
            rank=0,
        )


def test_validator_rejects_candidate_count_below_minimum() -> None:
    with pytest.raises(
        ValueError,
        match="candidate_count must be greater than or equal to 1",
    ):
        build_result(
            rank=None,
            candidate_count=0,
        )


def test_validator_rejects_rank_greater_than_candidate_count() -> None:
    with pytest.raises(
        ValueError,
        match="rank cannot be greater than candidate_count",
    ):
        build_result(
            rank=6,
            candidate_count=5,
        )