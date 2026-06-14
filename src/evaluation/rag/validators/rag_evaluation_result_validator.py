from __future__ import annotations

from datetime import datetime

from src.domain.validators.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.rag.schemas.rag_evaluation_result_schema import (
    RAG_EVALUATION_RESULT_SCHEMA,
)


class RAGEvaluationResultValidator:
    """
    RAGEvaluationResult validation service.
    """

    @staticmethod
    def validate(
        *,
        result_id: str,
        experiment_id: str,
        benchmark_id: str,
        benchmark_name: str,
        benchmark_version: str,
        sample_id: str,
        model_name: str,
        retriever_name: str,
        evaluator_name: str,
        query: str,
        generated_answer: str,
        expected_answer: str | None,
        retrieved_context_count: int,
        relevant_context_count: int,
        retrieval_precision: float,
        retrieval_recall: float,
        context_relevance_score: float,
        faithfulness_score: float,
        answer_relevance_score: float,
        answer_correctness_score: float,
        overall_score: float,
        hallucination_detected: bool,
        passed: bool,
        latency_ms: float,
        created_at: datetime,
        interpretation: str,
        notes: str | None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "result_id": result_id,
                "experiment_id": experiment_id,
                "benchmark_id": benchmark_id,
                "benchmark_name": benchmark_name,
                "benchmark_version": benchmark_version,
                "sample_id": sample_id,
                "model_name": model_name,
                "retriever_name": retriever_name,
                "evaluator_name": evaluator_name,
                "query": query,
                "generated_answer": generated_answer,
                "expected_answer": expected_answer,
                "retrieved_context_count": (
                    retrieved_context_count
                ),
                "relevant_context_count": (
                    relevant_context_count
                ),
                "retrieval_precision": retrieval_precision,
                "retrieval_recall": retrieval_recall,
                "context_relevance_score": (
                    context_relevance_score
                ),
                "faithfulness_score": faithfulness_score,
                "answer_relevance_score": (
                    answer_relevance_score
                ),
                "answer_correctness_score": (
                    answer_correctness_score
                ),
                "overall_score": overall_score,
                "hallucination_detected": (
                    hallucination_detected
                ),
                "passed": passed,
                "latency_ms": latency_ms,
                "created_at": created_at,
                "interpretation": interpretation,
                "notes": notes,
            },
            schema=RAG_EVALUATION_RESULT_SCHEMA,
            error_factory=EvaluationValidationError,
        )

        if (
            relevant_context_count
            > retrieved_context_count
        ):
            raise EvaluationValidationError(
                "relevant_context_count cannot exceed "
                "retrieved_context_count."
            )