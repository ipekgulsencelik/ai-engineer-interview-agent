from __future__ import annotations

from src.evaluation.rag.calculators.lexical_overlap_calculator import (
    LexicalOverlapCalculator,
)


class AnswerRelevancyScoreCalculator:
    """
    Calculates answer relevancy score.
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
        question_tokens: set[str],
        answer_tokens: set[str],
    ) -> float:
        return self._overlap_calculator.calculate(
            answer_tokens=question_tokens,
            context_tokens=answer_tokens,
        )