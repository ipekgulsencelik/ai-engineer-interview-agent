import pytest

from src.domain.entities.question import Question
from src.domain.enums.level import Level
from src.domain.enums.question_category import QuestionCategory
from src.domain.enums.question_type import QuestionType
from src.domain.policies.highest_score_selection_policy import (
    HighestScoreSelectionPolicy,
)
from src.domain.results.ranked_candidate import RankedCandidate
from src.domain.results.selection_breakdown import SelectionBreakdown


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


def build_candidate(
    *,
    final_score: float,
    rank: int,
) -> RankedCandidate:
    return RankedCandidate(
        question=build_question(
            id=f"q_{rank}",
        ),
        final_score=final_score,
        breakdown=build_breakdown(
            final_score=final_score,
        ),
        rank=rank,
    )


def test_policy_selects_first_ranked_candidate() -> None:
    policy = HighestScoreSelectionPolicy()

    ranked_candidates = [
        build_candidate(
            final_score=0.95,
            rank=1,
        ),
        build_candidate(
            final_score=0.82,
            rank=2,
        ),
        build_candidate(
            final_score=0.71,
            rank=3,
        ),
    ]

    selected = policy.select(
        ranked_candidates=ranked_candidates,
    )

    assert selected == ranked_candidates[0]
    assert selected.rank == 1
    assert selected.final_score == 0.95


def test_policy_rejects_empty_candidate_list() -> None:
    policy = HighestScoreSelectionPolicy()

    with pytest.raises(
        ValueError,
        match="ranked_candidates cannot be empty",
    ):
        policy.select(
            ranked_candidates=[],
        )


def test_policy_rejects_invalid_candidate_collection_type() -> None:
    policy = HighestScoreSelectionPolicy()

    with pytest.raises(
        TypeError,
        match="ranked_candidates must be a list",
    ):
        policy.select(
            ranked_candidates="invalid",
        )


def test_policy_rejects_invalid_candidate_items() -> None:
    policy = HighestScoreSelectionPolicy()

    with pytest.raises(
        TypeError,
        match="All ranked_candidates items must be RankedCandidate instances",
    ):
        policy.select(
            ranked_candidates=[
                object(),
            ],
        )