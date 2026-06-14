from __future__ import annotations

from src.evaluation.rag.calculators.rag_average_metric_calculator import (
    RAGAverageMetricCalculator,
)


class TurnRAGScoreCalculator:
    """
    Calculates overall score for one conversation turn.
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
        faithfulness_score: float,
        answer_relevancy_score: float,
        context_precision_score: float,
    ) -> float:
        return self._average_calculator.calculate(
            values=(
                faithfulness_score,
                answer_relevancy_score,
                context_precision_score,
            )
        )