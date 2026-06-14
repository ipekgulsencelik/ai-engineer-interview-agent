from __future__ import annotations

from src.evaluation.rag.calculators.lexical_overlap_calculator import (
    LexicalOverlapCalculator,
)


class ContextPrecisionScoreCalculator:
    """
    Calculates context precision score.
    """

    def __init__(
        self,
        *,
        overlap_calculator: (
            LexicalOverlapCalculator | None
        ) = None,
    ) -> None:
        self._overlap_calculator = (
            overlap_calculator
            or LexicalOverlapCalculator()
        )

    def calculate(
        self,
        *,
        answer_tokens: set[str],
        context_tokens: set[str],
    ) -> float:
        return self._overlap_calculator.calculate(
            answer_tokens=context_tokens,
            context_tokens=answer_tokens,
        )