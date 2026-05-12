from __future__ import annotations

from src.application.policies.selection_policy import SelectionPolicy
from src.domain.results.ranked_candidate import RankedCandidate
from src.domain.validators.ranked_candidate_list_validator import (
    RankedCandidateListValidator,
)


class HighestScoreSelectionPolicy(SelectionPolicy):
    """
    Highest scored ranked candidate selection policy.
    """

    def select(
        self,
        *,
        ranked_candidates: list[RankedCandidate],
    ) -> RankedCandidate:
        RankedCandidateListValidator.validate(
            ranked_candidates,
        )

        return ranked_candidates[0]