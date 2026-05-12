import pytest

from src.domain.entities.question import Question
from src.domain.enums.level import Level
from src.domain.enums.question_category import QuestionCategory
from src.domain.enums.question_type import QuestionType
from src.domain.results.ranked_candidate import RankedCandidate
from src.domain.results.selection_breakdown import SelectionBreakdown
from src.domain.validators.ranked_candidate_validator import (
    RankedCandidateValidator,
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


def build_candidate(**overrides) -> RankedCandidate:
    payload = {
        "question": build_question(),
        "final_score": 0.82,
        "breakdown": build_breakdown(),
        "rank": 1,
    }

    payload.update(overrides)

    return RankedCandidate(**payload)


def test_validator_accepts_valid_ranked_candidate() -> None:
    candidate = build_candidate()

    RankedCandidateValidator.validate(candidate)


def test_validator_rejects_non_ranked_candidate_instance() -> None:
    with pytest.raises(
        TypeError,
        match="candidate must be a RankedCandidate instance",
    ):
        RankedCandidateValidator.validate(object())


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        ("question", object()),
        ("final_score", "0.82"),
        ("breakdown", object()),
        ("rank", "1"),
    ],
)
def test_validator_rejects_invalid_field_types(
    field_name: str,
    value,
) -> None:
    with pytest.raises(TypeError):
        build_candidate(
            **{
                field_name: value,
            }
        )


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        ("final_score", True),
        ("rank", False),
    ],
)
def test_validator_rejects_bool_values_for_numeric_fields(
    field_name: str,
    value: bool,
) -> None:
    with pytest.raises(TypeError):
        build_candidate(
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
        build_candidate(
            final_score=value,
        )


def test_validator_rejects_negative_final_score() -> None:
    with pytest.raises(
        ValueError,
        match="final_score must be greater than or equal to 0.0",
    ):
        build_candidate(
            final_score=-0.1,
        )


def test_validator_rejects_rank_below_minimum() -> None:
    with pytest.raises(
        ValueError,
        match="rank must be greater than or equal to 1",
    ):
        build_candidate(
            rank=0,
        )