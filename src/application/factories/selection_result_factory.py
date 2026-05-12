from __future__ import annotations

from src.application.ports.clock import Clock
from src.application.validators.selection_result_factory_validator import (
    SelectionResultFactoryValidator,
)
from src.application.policies.selection_policy import SelectionPolicy
from src.domain.results.ranked_candidate import RankedCandidate
from src.domain.results.selection_result import SelectionResult
from src.domain.scoring.scoring_context import ScoringContext


class SelectionResultFactory:
    """
    RankedCandidate listesinden final SelectionResult üretir.
    """

    def __init__(
        self,
        selection_policy: SelectionPolicy,
        clock: Clock,
    ) -> None:
        SelectionResultFactoryValidator.validate_selection_policy(
            selection_policy,
        )
        SelectionResultFactoryValidator.validate_clock(
            clock,
        )

        self._selection_policy = selection_policy
        self._clock = clock

    def build(
        self,
        *,
        ranked_candidates: list[RankedCandidate],
    ) -> SelectionResult:
        SelectionResultFactoryValidator.validate_ranked_candidates(
            ranked_candidates,
        )

        return self._selection_policy.select(
            ranked_candidates=ranked_candidates,
            context=ScoringContext(),
        )