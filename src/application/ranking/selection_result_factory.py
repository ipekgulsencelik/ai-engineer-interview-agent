from __future__ import annotations

from src.domain.retrieval.question_search_result import (
    QuestionSearchResult,
)
from src.domain.results.selection_result import (
    SelectionResult,
)
from src.domain.value_objects.selection_breakdown import (
    SelectionBreakdown,
)


class SelectionResultFactory:
    """
    SelectionResult creation factory.
    """

    @staticmethod
    def create(
        *,
        search_result: QuestionSearchResult,
        breakdown: SelectionBreakdown,
        rank: int,
        candidate_count: int,
    ) -> SelectionResult:
        return SelectionResult(
            question=search_result.question,
            final_score=breakdown.final_score,
            breakdown=breakdown,
            rank=rank,
            candidate_count=candidate_count,
        )