from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from src.domain.results.ranked_candidate import RankedCandidate


class SelectionPolicy(ABC):
    """Ranked candidate listesinden final adayı seçer."""

    @abstractmethod
    def select(
        self,
        *,
        ranked_candidates: list[RankedCandidate],
    ) -> RankedCandidate:
        pass
