from datetime import datetime, timezone

import pytest

from src.domain.entities.question import Question
from src.domain.enums.level import Level
from src.domain.enums.question_category import QuestionCategory
from src.domain.enums.question_type import QuestionType
from src.domain.results.selection_breakdown import SelectionBreakdown
from src.domain.results.selection_result import SelectionResult


def build_question(**overrides) -> Question:
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


def build_selection_result(**overrides) -> SelectionResult:
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


def test_selection_result_can_be_created_with_valid_data() -> None:
    result = build_selection_result()

    assert isinstance(result.question, Question)
    assert result.final_score == 0.82
    assert isinstance(result.breakdown, SelectionBreakdown)
    assert result.rank == 1
    assert result.candidate_count == 5
    assert result.selected_at.tzinfo is not None


def test_selection_result_uses_timezone_aware_default_selected_at() -> None:
    result = SelectionResult(
        question=build_question(),
        final_score=0.82,
        breakdown=build_breakdown(),
    )

    assert result.selected_at.tzinfo is not None
    assert result.selected_at.utcoffset() is not None


def test_selection_result_can_be_created_without_optional_rank_and_count() -> None:
    result = SelectionResult(
        question=build_question(),
        final_score=0.82,
        breakdown=build_breakdown(),
    )

    assert result.rank is None
    assert result.candidate_count is None


def test_selection_result_is_immutable() -> None:
    result = build_selection_result()

    with pytest.raises(Exception):
        result.final_score = 0.1


def test_selection_result_final_score_cannot_be_negative() -> None:
    with pytest.raises(
        ValueError,
        match="final_score must be greater than or equal to 0.0",
    ):
        build_selection_result(
            final_score=-0.1,
        )


def test_selection_result_rank_cannot_be_below_minimum() -> None:
    with pytest.raises(
        ValueError,
        match="rank must be greater than or equal to 1",
    ):
        build_selection_result(
            rank=0,
        )


def test_selection_result_candidate_count_cannot_be_below_minimum() -> None:
    with pytest.raises(
        ValueError,
        match="candidate_count must be greater than or equal to 1",
    ):
        build_selection_result(
            rank=None,
            candidate_count=0,
        )


def test_selection_result_selected_at_must_be_timezone_aware() -> None:
    with pytest.raises(
        ValueError,
        match="selected_at must be timezone-aware",
    ):
        build_selection_result(
            selected_at=datetime.now(),
        )


def test_selection_result_rank_cannot_be_greater_than_candidate_count() -> None:
    with pytest.raises(
        ValueError,
        match="rank cannot be greater than candidate_count",
    ):
        build_selection_result(
            rank=6,
            candidate_count=5,
        )