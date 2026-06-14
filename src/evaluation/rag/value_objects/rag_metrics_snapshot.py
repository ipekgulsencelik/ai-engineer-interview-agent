from __future__ import annotations

from dataclasses import dataclass

from src.evaluation.rag.validators.rag_metrics_snapshot_validator import (
    RAGMetricsSnapshotValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class RAGMetricsSnapshot:
    """
    Immutable RAG metrics snapshot.

    Represents aggregated average metric values
    calculated from RAG evaluation results.
    """

    average_retrieval_precision: float

    average_retrieval_recall: float

    average_context_relevance_score: float

    average_faithfulness_score: float

    average_answer_relevance_score: float

    average_answer_correctness_score: float

    average_overall_score: float

    def __post_init__(
        self,
    ) -> None:
        RAGMetricsSnapshotValidator.validate(
            average_retrieval_precision=(
                self.average_retrieval_precision
            ),
            average_retrieval_recall=(
                self.average_retrieval_recall
            ),
            average_context_relevance_score=(
                self.average_context_relevance_score
            ),
            average_faithfulness_score=(
                self.average_faithfulness_score
            ),
            average_answer_relevance_score=(
                self.average_answer_relevance_score
            ),
            average_answer_correctness_score=(
                self.average_answer_correctness_score
            ),
            average_overall_score=(
                self.average_overall_score
            ),
        )