from __future__ import annotations

from src.evaluation.rag.calculators.rag_average_metric_calculator import (
    RAGAverageMetricCalculator,
)


class ConversationRAGScoreCalculator:
    """
    Calculates overall score for a conversation.
    """

    def __init__(
        self,
        *,
        average_calculator: (
            RAGAverageMetricCalculator | None
        ) = None,
    ) -> None:
        self._average_calculator = (
            average_calculator
            or RAGAverageMetricCalculator()
        )

    def calculate(
        self,
        *,
        turn_scores: tuple[
            float,
            ...,
        ],
    ) -> float:
        return self._average_calculator.calculate(
            values=turn_scores,
        )