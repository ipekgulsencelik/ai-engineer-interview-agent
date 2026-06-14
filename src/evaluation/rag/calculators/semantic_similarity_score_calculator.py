from __future__ import annotations

from src.evaluation.rag.calculators.lexical_overlap_calculator import (
    LexicalOverlapCalculator,
)


class SemanticSimilarityScoreCalculator:
    """
    Calculates semantic similarity score.

    Uses lexical overlap as a deterministic baseline.
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
        reference_tokens: set[str],
        candidate_tokens: set[str],
    ) -> float:
        return self._overlap_calculator.calculate(
            answer_tokens=reference_tokens,
            context_tokens=candidate_tokens,
        )