from __future__ import annotations

import pytest

from src.application.policies.highest_score_selection_policy import (
    HighestScoreSelectionPolicy,
)
from src.domain.entities.question import Question
from src.domain.enums.level import Level
from src.domain.enums.question_category import (
    QuestionCategory,
)
from src.domain.enums.question_type import (
    QuestionType,
)
from src.domain.results.ranked_candidate import RankedCandidate
from src.domain.results.selection_breakdown import (
    SelectionBreakdown,
)


def build_question(question_id: str) -> Question:
    return Question(
        id=question_id,
        text=f"Question {question_id}",
        category=QuestionCategory.RAG,
        level=Level.JR,
        difficulty=1,
        question_type=QuestionType.CONCEPTUAL,
        expected_points=[],
        keywords=[],
    )


def build_breakdown(final_score: float) -> SelectionBreakdown:
    return SelectionBreakdown(
        level_score=1.0,
        market_score=1.0,
        cv_gap_score=1.0,
        difficulty_score=1.0,
        diversity_score=1.0,
        fatigue_score=1.0,
        final_score=final_score,
    )


def build_candidate(
    *,
    question_id: str,
    rank: int,
    final_score: float,
) -> RankedCandidate:
    return RankedCandidate(
        question=build_question(question_id),
        breakdown=build_breakdown(final_score),
        final_score=final_score,
        rank=rank,
    )


def test_select_returns_highest_ranked_candidate() -> None:
    policy = HighestScoreSelectionPolicy()

    first_candidate = build_candidate(
        question_id="q1",
        rank=1,
        final_score=0.95,
    )

    second_candidate = build_candidate(
        question_id="q2",
        rank=2,
        final_score=0.84,
    )

    result = policy.select(
        ranked_candidates=[
            first_candidate,
            second_candidate,
        ],
    )

    assert result is first_candidate


def test_select_is_deterministic() -> None:
    policy = HighestScoreSelectionPolicy()

    candidates = [
        build_candidate(
            question_id="q1",
            rank=1,
            final_score=0.95,
        ),
        build_candidate(
            question_id="q2",
            rank=2,
            final_score=0.82,
        ),
    ]

    first_result = policy.select(
        ranked_candidates=candidates,
    )

    second_result = policy.select(
        ranked_candidates=candidates,
    )

    assert first_result is second_result


def test_select_rejects_empty_candidate_list() -> None:
    policy = HighestScoreSelectionPolicy()

    with pytest.raises(ValueError):
        policy.select(
            ranked_candidates=[],
        )


def test_select_rejects_non_list_input() -> None:
    policy = HighestScoreSelectionPolicy()

    with pytest.raises(TypeError):
        policy.select(
            ranked_candidates="invalid",  # type: ignore[arg-type]
        )


def test_select_rejects_invalid_candidate_items() -> None:
    policy = HighestScoreSelectionPolicy()

    with pytest.raises(TypeError):
        policy.select(
            ranked_candidates=[
                object(),
            ],  # type: ignore[list-item]
        )
