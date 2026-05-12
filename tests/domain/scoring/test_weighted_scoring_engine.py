from __future__ import annotations

import pytest

from src.domain.entities.question import Question
from src.domain.enums.difficulty import Difficulty
from src.domain.enums.level import Level
from src.domain.enums.question_category import (
    QuestionCategory,
)
from src.domain.enums.question_type import (
    QuestionType,
)
from src.domain.scoring.final_score_calculator import (
    FinalScoreCalculator,
)
from src.domain.policies.cv_gap_score_policy import (
    CvGapScorePolicy,
)
from src.domain.policies.difficulty_score_policy import (
    DifficultyScorePolicy,
)
from src.domain.policies.diversity_score_policy import (
    DiversityScorePolicy,
)
from src.domain.policies.fatigue_score_policy import (
    FatigueScorePolicy,
)
from src.domain.policies.level_score_policy import (
    LevelScorePolicy,
)
from src.domain.policies.market_score_policy import (
    MarketScorePolicy,
)
from src.domain.scoring.scoring_context import (
    ScoringContext,
)
from src.domain.scoring.weighted_scoring_engine import (
    WeightedScoringEngine,
)
from src.domain.policies.weighted_scoring_policy import (
    WeightedScoringPolicy,
)


def build_engine() -> WeightedScoringEngine:
    policy = WeightedScoringPolicy(
        level_score_policy=LevelScorePolicy(),
        market_score_policy=MarketScorePolicy(),
        cv_gap_score_policy=CvGapScorePolicy(),
        difficulty_score_policy=DifficultyScorePolicy(),
        diversity_score_policy=DiversityScorePolicy(),
        fatigue_score_policy=FatigueScorePolicy(),
        final_score_calculator=FinalScoreCalculator(),
    )

    return WeightedScoringEngine(
        policy=policy,
    )


def build_question() -> Question:
    return Question(
        id="q1",
        text="Explain RAG architecture.",
        category=QuestionCategory.RAG,
        level=Level.MID,
        difficulty=Difficulty.MEDIUM,
        question_type=QuestionType.CONCEPTUAL,
        expected_points=[
            "retrieval",
            "generation",
        ],
        keywords=[
            "vector db",
            "embedding",
        ],
        market_weight=0.9,
    )


def build_context() -> ScoringContext:
    return ScoringContext(
        current_level=Level.MID,
        cv_skills=[
            "python",
        ],
        asked_question_ids=set(),
        recent_scores=[7.5, 8.0],
    )


def test_score_returns_scoring_breakdown() -> None:
    engine = build_engine()

    result = engine.score(
        question=build_question(),
        context=build_context(),
    )

    assert result.final_score > 0.0
    assert result.level_score >= 0.0
    assert result.market_score >= 0.0
    assert result.cv_gap_score >= 0.0
    assert result.difficulty_score >= 0.0
    assert result.diversity_score >= 0.0
    assert result.fatigue_score >= 0.0


def test_score_rejects_invalid_question() -> None:
    engine = build_engine()

    with pytest.raises(TypeError):
        engine.score(
            question="invalid",  # type: ignore[arg-type]
            context=build_context(),
        )


def test_score_rejects_invalid_context() -> None:
    engine = build_engine()

    with pytest.raises(TypeError):
        engine.score(
            question=build_question(),
            context="invalid",  # type: ignore[arg-type]
        )


def test_score_is_deterministic() -> None:
    engine = build_engine()

    first = engine.score(
        question=build_question(),
        context=build_context(),
    )

    second = engine.score(
        question=build_question(),
        context=build_context(),
    )

    assert first == second