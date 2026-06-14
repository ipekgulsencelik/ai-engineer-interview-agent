from __future__ import annotations

from src.evaluation.rag.calculators.lexical_overlap_calculator import (
    LexicalOverlapCalculator,
)


class ContextRecallScoreCalculator:
    """
    Calculates context recall score.
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
        expected_context_tokens: set[str],
        retrieved_context_tokens: set[str],
    ) -> float:
        return self._overlap_calculator.calculate(
            answer_tokens=(
                expected_context_tokens
            ),
            context_tokens=(
                retrieved_context_tokens
            ),
        )