"""Executable regression tests for the question ranking pipeline."""

from __future__ import annotations

from typing import cast

import pytest

from src.application.ports.scoring_engine import ScoringEngine
from src.application.rankers.candidate_question_ranker import (
    CandidateQuestionRanker,
)
from src.domain.entities.question import Question
from src.domain.enums.level import Level
from src.domain.enums.question_category import QuestionCategory
from src.domain.enums.question_type import QuestionType
from src.domain.results.selection_breakdown import SelectionBreakdown
from src.domain.scoring.scoring_context import ScoringContext


class StubScoringEngine(ScoringEngine):
    """Deterministic scoring port implementation requiring no external services."""

    def __init__(self, scores: dict[str, float]) -> None:
        self._scores = scores
        self.scored_ids: list[str] = []

    def score(
        self,
        *,
        question: Question,
        context: ScoringContext,
    ) -> SelectionBreakdown:
        self.scored_ids.append(question.id)
        return SelectionBreakdown(
            level_score=0.5,
            semantic_score=0.5,
            market_score=0.5,
            cv_gap_score=0.5,
            difficulty_score=0.5,
            diversity_score=0.5,
            fatigue_score=0.5,
            final_score=self._scores[question.id],
        )


def _question(question_id: str) -> Question:
    return Question(
        id=question_id,
        text=f"Explain {question_id}",
        category=QuestionCategory.RAG,
        level=Level.MID,
        difficulty=2,
        question_type=QuestionType.CONCEPTUAL,
    )


def test_ranker_orders_by_score_and_preserves_breakdown() -> None:
    engine = StubScoringEngine({"low": 0.2, "high": 0.9, "mid": 0.5})
    questions = [_question("low"), _question("high"), _question("mid")]

    results = CandidateQuestionRanker(scoring_engine=engine).rank(
        questions=questions,
        context=ScoringContext(),
    )

    assert [result.question.id for result in results] == ["high", "mid", "low"]
    assert [result.rank for result in results] == [1, 2, 3]
    assert [result.final_score for result in results] == [0.9, 0.5, 0.2]
    assert [result.breakdown.final_score for result in results] == [
        0.9,
        0.5,
        0.2,
    ]
    assert engine.scored_ids == ["low", "high", "mid"]
    assert [question.id for question in questions] == ["low", "high", "mid"]


def test_equal_scores_preserve_original_candidate_order() -> None:
    engine = StubScoringEngine({"first": 0.8, "second": 0.8})
    results = CandidateQuestionRanker(scoring_engine=engine).rank(
        questions=[_question("second"), _question("first")],
        context=ScoringContext(),
    )

    assert [result.question.id for result in results] == ["second", "first"]
    assert [result.rank for result in results] == [1, 2]


def test_empty_candidates_do_not_call_scoring_engine() -> None:
    engine = StubScoringEngine({})
    results = CandidateQuestionRanker(scoring_engine=engine).rank(
        questions=[],
        context=ScoringContext(),
    )

    assert results == []
    assert engine.scored_ids == []


def test_ranker_rejects_invalid_scoring_engine() -> None:
    with pytest.raises(TypeError, match="ScoringEngine"):
        CandidateQuestionRanker(scoring_engine=cast(ScoringEngine, object()))


def test_ranker_rejects_non_question_candidates() -> None:
    ranker = CandidateQuestionRanker(scoring_engine=StubScoringEngine({}))

    with pytest.raises(TypeError, match="Question"):
        ranker.rank(
            questions=cast(list[Question], [object()]),
            context=ScoringContext(),
        )
