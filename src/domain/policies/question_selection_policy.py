from __future__ import annotations

from src.domain.policies.highest_score_selection_policy import (
    HighestScoreSelectionPolicy,
)
from src.domain.results.selection_result import (
    SelectionResult,
)
from src.domain.validators.selection_candidate_validator import (
    SelectionCandidateValidator,
)


class QuestionSelectionPolicy:
    """
    Final ranked candidate selection policy.
    """

    def __init__(
        self,
        *,
        selection_strategy: HighestScoreSelectionPolicy | None = None,
    ) -> None:
        self._selection_strategy = (
            selection_strategy
            or HighestScoreSelectionPolicy()
        )

    def select_best_candidate(
        self,
        *,
        ranked_candidates: list[SelectionResult],
    ) -> SelectionResult:
        SelectionCandidateValidator.validate(
            ranked_candidates=ranked_candidates,
        )

        return self._selection_strategy.select(
            ranked_candidates=ranked_candidates,
        )