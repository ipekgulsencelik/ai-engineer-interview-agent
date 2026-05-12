from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from src.domain.results.ranked_candidate import RankedCandidate
from src.domain.results.selection_result import SelectionResult
from src.domain.scoring.scoring_context import ScoringContext


class SelectionPolicy(ABC):
    """Ranked candidate listesinden final selection sonucu üretir."""

    @abstractmethod
    def select(
        self,
        *,
        ranked_candidates: list[RankedCandidate],
        context: ScoringContext,
    ) -> SelectionResult:
        pass
