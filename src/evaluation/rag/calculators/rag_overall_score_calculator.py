from __future__ import annotations

from src.evaluation.rag.calculators.rag_average_metric_calculator import (
    RAGAverageMetricCalculator,
)


class RAGOverallScoreCalculator:
    """
    Calculates sample-level overall RAG score.
    """

    def __init__(
        self,
        *,
        average_calculator: RAGAverageMetricCalculator | None = None,
    ) -> None:
        self._average_calculator = (
            average_calculator
            or RAGAverageMetricCalculator()
        )

    def calculate(
        self,
        *,
        retrieval_precision: float,
        retrieval_recall: float,
        context_relevance_score: float,
        faithfulness_score: float,
        answer_relevance_score: float,
        answer_correctness_score: float,
    ) -> float:
        return self._average_calculator.calculate(
            values=(
                retrieval_precision,
                retrieval_recall,
                context_relevance_score,
                faithfulness_score,
                answer_relevance_score,
                answer_correctness_score,
            )
        )