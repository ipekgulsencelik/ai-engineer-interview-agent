from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from src.domain.entities.question import Question
from src.domain.results.selection_breakdown import (
    SelectionBreakdown,
)
from src.domain.scoring.scoring_context import (
    ScoringContext,
)


class ScoringEngine(ABC):
    """
    Question scoring behavior contract.
    """

    @abstractmethod
    def score(
        self,
        *,
        question: Question,
        context: ScoringContext,
    ) -> SelectionBreakdown:
        """
        Verilen question için explainable scoring sonucu üretir.
        """
        pass