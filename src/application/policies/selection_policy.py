from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from src.domain.results.ranked_candidate import RankedCandidate


class SelectionPolicy(ABC):
    """
    Ranked candidate listesi içerisinden final candidate seçimini yapan
    domain policy abstraction'ı.
    """

    @abstractmethod
    def select(
        self,
        *,
        ranked_candidates: list[RankedCandidate],
    ) -> RankedCandidate:
        """
        Ranked candidate listesi içerisinden final candidate'i seçer.
        """
        pass