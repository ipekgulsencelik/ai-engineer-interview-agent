from __future__ import annotations

from src.evaluation.rag.calculators.rag_average_metric_calculator import (
    RAGAverageMetricCalculator,
)
from src.evaluation.rag.value_objects.rag_evaluation_result import (
    RAGEvaluationResult,
)
from src.evaluation.rag.value_objects.rag_metrics_snapshot import (
    RAGMetricsSnapshot,
)


class RAGMetricsAggregator:
    """
    Aggregates RAG evaluation metrics into a
    metrics snapshot.
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

    def aggregate(
        self,
        *,
        results: tuple[
            RAGEvaluationResult,
            ...,
        ],
    ) -> RAGMetricsSnapshot:
        return RAGMetricsSnapshot(
            average_retrieval_precision=(
                self._average_calculator.calculate(
                    values=tuple(
                        result.retrieval_precision
                        for result in results
                    ),
                )
            ),
            average_retrieval_recall=(
                self._average_calculator.calculate(
                    values=tuple(
                        result.retrieval_recall
                        for result in results
                    ),
                )
            ),
            average_context_relevance_score=(
                self._average_calculator.calculate(
                    values=tuple(
                        result.context_relevance_score
                        for result in results
                    ),
                )
            ),
            average_faithfulness_score=(
                self._average_calculator.calculate(
                    values=tuple(
                        result.faithfulness_score
                        for result in results
                    ),
                )
            ),
            average_answer_relevance_score=(
                self._average_calculator.calculate(
                    values=tuple(
                        result.answer_relevance_score
                        for result in results
                    ),
                )
            ),
            average_answer_correctness_score=(
                self._average_calculator.calculate(
                    values=tuple(
                        result.answer_correctness_score
                        for result in results
                    ),
                )
            ),
            average_overall_score=(
                self._average_calculator.calculate(
                    values=tuple(
                        result.overall_score
                        for result in results
                    ),
                )
            ),
        )