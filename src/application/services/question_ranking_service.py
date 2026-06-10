from __future__ import annotations

from src.domain.constants.ranking import (
    INITIAL_CANDIDATE_RANK,
    RANKING_START_INDEX,
)
from src.application.ranking.selection_result_factory import (
    SelectionResultFactory,
)
from src.domain.results.selection_result import (
    SelectionResult,
)
from src.domain.retrieval.question_search_result import (
    QuestionSearchResult,
)
from src.domain.scoring.retrieval_score_calculator import (
    RetrievalScoreCalculator,
)


class QuestionRankingService:
    """
    Semantic retrieval candidate ranking service.
    """

    def __init__(
        self,
        *,
        score_calculator: RetrievalScoreCalculator | None = None,
        result_factory: SelectionResultFactory | None = None,
    ) -> None:
        self._score_calculator = (
            score_calculator
            or RetrievalScoreCalculator()
        )
        self._result_factory = (
            result_factory
            or SelectionResultFactory()
        )

    def rank_candidates(
        self,
        *,
        search_results: list[QuestionSearchResult],
        target_difficulty: int,
    ) -> list[SelectionResult]:
    
        candidate_count = len(search_results)

        scored_results = [
            self._result_factory.create(
                search_result=search_result,
                breakdown=self._score_calculator.calculate(
                    search_result=search_result,
                    target_difficulty=target_difficulty,
                ),
                rank=INITIAL_CANDIDATE_RANK,
                candidate_count=candidate_count,
            )
            for search_result in search_results
        ]

        sorted_results = sorted(
            scored_results,
            key=lambda result: result.final_score,
            reverse=True,
        )

        return [
            SelectionResult(
                question=result.question,
                final_score=result.final_score,
                breakdown=result.breakdown,
                rank=index,
                candidate_count=candidate_count,
                selected_at=result.selected_at,
            )
            for index, result in enumerate(
                sorted_results,
                start=RANKING_START_INDEX,
            )
        ]