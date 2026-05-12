from __future__ import annotations

from src.application.policies.selection_policy import (
    SelectionPolicy,
)
from src.domain.results.ranked_candidate import (
    RankedCandidate,
)
from src.domain.results.selection_result import (
    SelectionResult,
)
from src.domain.scoring.scoring_context import (
    ScoringContext,
)
from src.domain.validators.ranked_candidate_list_validator import (
    RankedCandidateListValidator,
)


class HighestScoreSelectionPolicy(SelectionPolicy):
    """
    Selects the highest-ranked candidate.
    """

    def select(
        self,
        *,
        ranked_candidates: list[RankedCandidate],
        context: ScoringContext,
    ) -> SelectionResult:
        RankedCandidateListValidator.validate(
            ranked_candidates,
        )

        selected_candidate = ranked_candidates[0]

        return SelectionResult(
            question=selected_candidate.question,
            final_score=selected_candidate.final_score,
            breakdown=selected_candidate.breakdown,
            rank=selected_candidate.rank,
            candidate_count=len(ranked_candidates),
        )
