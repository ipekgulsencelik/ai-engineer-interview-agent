from __future__ import annotations

from src.domain.results.ranked_candidate import RankedCandidate
from src.domain.results.selection_result import SelectionResult


class SelectionResultBuilder:
    """
    SelectionResult immutable snapshot üretir.
    """

    @staticmethod
    def build(
        *,
        selected_candidate: RankedCandidate,
        candidate_count: int,
    ) -> SelectionResult:
        return SelectionResult(
            question=selected_candidate.question,
            breakdown=selected_candidate.breakdown,
            final_score=selected_candidate.final_score,
            rank=selected_candidate.rank,
            candidate_count=candidate_count,
        )