from __future__ import annotations

from src.domain.constants.retrieval_scoring import (
    DEFAULT_CV_GAP_SCORE,
    DEFAULT_DIVERSITY_SCORE,
    DEFAULT_FATIGUE_SCORE,
    DEFAULT_LEVEL_SCORE,
    DIFFICULTY_SCORE_WEIGHT,
    DIVERSITY_SCORE_WEIGHT,
    MARKET_SCORE_WEIGHT,
    SEMANTIC_SCORE_WEIGHT,
)
from src.domain.retrieval.question_search_result import (
    QuestionSearchResult,
)
from src.domain.scoring.difficulty_match_score_policy import (
    DifficultyMatchScorePolicy,
)
from src.domain.scoring.market_score_policy import (
    MarketScorePolicy,
)
from src.domain.scoring.normalized_score_clamper import (
    NormalizedScoreClamper,
)
from src.domain.value_objects.selection_breakdown import (
    SelectionBreakdown,
)


class RetrievalScoreCalculator:
    """
    Weighted retrieval scoring policy.
    """

    @classmethod
    def calculate(
        cls,
        *,
        search_result: QuestionSearchResult,
        target_difficulty: int,
        diversity_score: float = DEFAULT_DIVERSITY_SCORE,
    ) -> SelectionBreakdown:
        semantic_score = search_result.score

        market_score = MarketScorePolicy.calculate(
            market_weight=search_result.question.market_weight,
        )

        difficulty_score = (
            DifficultyMatchScorePolicy.calculate(
                question_difficulty=(
                    search_result.question.difficulty
                ),
                target_difficulty=target_difficulty,
            )
        )

        normalized_diversity_score = (
            NormalizedScoreClamper.clamp(
                score=diversity_score,
            )
        )

        final_score = cls._calculate_final_score(
            semantic_score=semantic_score,
            market_score=market_score,
            difficulty_score=difficulty_score,
            diversity_score=normalized_diversity_score,
        )

        return SelectionBreakdown(
            level_score=DEFAULT_LEVEL_SCORE,
            semantic_score=semantic_score,
            market_score=market_score,
            cv_gap_score=DEFAULT_CV_GAP_SCORE,
            difficulty_score=difficulty_score,
            diversity_score=normalized_diversity_score,
            fatigue_score=DEFAULT_FATIGUE_SCORE,
            final_score=NormalizedScoreClamper.clamp(
                score=final_score,
            ),
        )

    @staticmethod
    def _calculate_final_score(
        *,
        semantic_score: float,
        market_score: float,
        difficulty_score: float,
        diversity_score: float,
    ) -> float:
        return (
            semantic_score * SEMANTIC_SCORE_WEIGHT
            + market_score * MARKET_SCORE_WEIGHT
            + difficulty_score
            * DIFFICULTY_SCORE_WEIGHT
            + diversity_score
            * DIVERSITY_SCORE_WEIGHT
        )