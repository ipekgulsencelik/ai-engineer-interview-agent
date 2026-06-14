from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from src.evaluation.rag.entities.rag_evaluation_sample import (
    RAGEvaluationSample,
)
from src.evaluation.rag.value_objects.rag_evaluation_result import (
    RAGEvaluationResult,
)


class RAGEvaluationResultFactory:
    """
    Factory for sample-level RAG evaluation results.
    """

    @staticmethod
    def create(
        *,
        experiment_id: str,
        model_name: str,
        retriever_name: str,
        evaluator_name: str,
        sample: RAGEvaluationSample,
        generated_answer: str,
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
        notes: str | None = None,
    ) -> RAGEvaluationResult:
        return RAGEvaluationResult(
            result_id=str(
                uuid4(),
            ),
            experiment_id=experiment_id,
            benchmark_id=sample.benchmark_id,
            benchmark_name=sample.benchmark_name,
            benchmark_version=sample.benchmark_version,
            sample_id=sample.sample_id,
            model_name=model_name,
            retriever_name=retriever_name,
            evaluator_name=evaluator_name,
            query=sample.question,
            generated_answer=generated_answer,
            expected_answer=sample.expected_answer,
            retrieved_context_count=(
                retrieved_context_count
            ),
            relevant_context_count=(
                relevant_context_count
            ),
            retrieval_precision=retrieval_precision,
            retrieval_recall=retrieval_recall,
            context_relevance_score=(
                context_relevance_score
            ),
            faithfulness_score=faithfulness_score,
            answer_relevance_score=(
                answer_relevance_score
            ),
            answer_correctness_score=(
                answer_correctness_score
            ),
            overall_score=overall_score,
            hallucination_detected=(
                hallucination_detected
            ),
            passed=passed,
            latency_ms=latency_ms,
            created_at=created_at,
            interpretation=interpretation,
            notes=notes,
        )