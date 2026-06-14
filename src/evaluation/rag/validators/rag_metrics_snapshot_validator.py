from __future__ import annotations

from src.domain.validators.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.rag.schemas.rag_metrics_snapshot_schema import (
    RAG_METRICS_SNAPSHOT_SCHEMA,
)


class RAGMetricsSnapshotValidator:
    """
    RAGMetricsSnapshot validation service.
    """

    @staticmethod
    def validate(
        *,
        average_retrieval_precision: float,
        average_retrieval_recall: float,
        average_context_relevance_score: float,
        average_faithfulness_score: float,
        average_answer_relevance_score: float,
        average_answer_correctness_score: float,
        average_overall_score: float,
    ) -> None:
        SchemaValidator.validate(
            values={
                "average_retrieval_precision": (
                    average_retrieval_precision
                ),
                "average_retrieval_recall": (
                    average_retrieval_recall
                ),
                "average_context_relevance_score": (
                    average_context_relevance_score
                ),
                "average_faithfulness_score": (
                    average_faithfulness_score
                ),
                "average_answer_relevance_score": (
                    average_answer_relevance_score
                ),
                "average_answer_correctness_score": (
                    average_answer_correctness_score
                ),
                "average_overall_score": (
                    average_overall_score
                ),
            },
            schema=RAG_METRICS_SNAPSHOT_SCHEMA,
            error_factory=EvaluationValidationError,
        )