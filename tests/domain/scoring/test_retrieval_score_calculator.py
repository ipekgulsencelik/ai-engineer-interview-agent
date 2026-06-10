from __future__ import annotations

from src.domain.entities.question import Question
from src.domain.enums.level import Level
from src.domain.enums.question_category import QuestionCategory
from src.domain.enums.question_type import QuestionType
from src.domain.retrieval.question_search_result import QuestionSearchResult
from src.domain.scoring.difficulty_match_score_policy import DifficultyMatchScorePolicy
from src.domain.scoring.market_score_policy import MarketScorePolicy
from src.domain.scoring.retrieval_score_calculator import RetrievalScoreCalculator


def _search_result() -> QuestionSearchResult:
    question = Question(
        id="rag_mid_001",
        text="How would you improve retrieval quality?",
        category=QuestionCategory.RAG,
        level=Level.MID,
        question_type=QuestionType.CONCEPTUAL,
        difficulty=2,
        market_weight=0.8,
        expected_points=["retrieval", "embedding"],
    )

    return QuestionSearchResult(question=question, distance=0.2, score=0.8)


def test_calculate_should_return_selection_breakdown() -> None:
    result = RetrievalScoreCalculator.calculate(
        search_result=_search_result(),
        target_difficulty=2,
    )

    assert result.semantic_score == 0.8
    assert result.market_score == 0.8
    assert result.difficulty_score == 1.0
    assert result.final_score > 0


def test_market_weight_should_be_clamped() -> None:
    result = MarketScorePolicy.calculate(market_weight=5.0)

    assert result == 1.0


def test_difficulty_score_should_drop_by_distance() -> None:
    score = DifficultyMatchScorePolicy.calculate(
        question_difficulty=3,
        target_difficulty=1,
    )

    assert score == 0.8
