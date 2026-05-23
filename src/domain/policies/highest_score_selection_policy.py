from __future__ import annotations

from src.domain.results.selection_result import (
    SelectionResult,
)


class HighestScoreSelectionPolicy:
    """
    Highest score candidate selection strategy.
    """

    @staticmethod
    def select(
        *,
        ranked_candidates: list[SelectionResult],
    ) -> SelectionResult:
        return max(
            ranked_candidates,
            key=lambda candidate: (
                candidate.final_score,
                -candidate.rank
                if candidate.rank is not None
                else 0,
            ),
        )