from __future__ import annotations

from datetime import UTC
from datetime import datetime
from uuid import uuid4

from src.evaluation.rag.entities.rag_evaluation_report import (
    RAGEvaluationReport,
)
from src.evaluation.rag.value_objects.rag_evaluation_result import (
    RAGEvaluationResult,
)


class RAGEvaluationReportFactory:
    """
    Factory for creating RAG evaluation reports.
    """

    @staticmethod
    def create(
        *,
        experiment_id: str,
        benchmark_id: str,
        benchmark_name: str,
        benchmark_version: str,
        model_name: str,
        retriever_name: str,
        evaluator_name: str,
        results: tuple[
            RAGEvaluationResult,
            ...,
        ],
        sample_count: int,
        average_retrieval_precision: float,
        average_retrieval_recall: float,
        average_context_relevance_score: float,
        average_faithfulness_score: float,
        average_answer_relevance_score: float,
        average_answer_correctness_score: float,
        average_overall_score: float,
        hallucination_count: int,
        hallucination_rate: float,
        passed_count: int,
        failed_count: int,
        pass_rate: float,
        interpretation: str,
        generated_at: datetime | None = None,
        notes: str | None = None,
    ) -> RAGEvaluationReport:
        return RAGEvaluationReport(
            report_id=str(
                uuid4(),
            ),
            experiment_id=experiment_id,
            benchmark_id=benchmark_id,
            benchmark_name=benchmark_name,
            benchmark_version=benchmark_version,
            model_name=model_name,
            retriever_name=retriever_name,
            evaluator_name=evaluator_name,
            results=results,
            sample_count=sample_count,
            average_retrieval_precision=(
                average_retrieval_precision
            ),
            average_retrieval_recall=(
                average_retrieval_recall
            ),
            average_context_relevance_score=(
                average_context_relevance_score
            ),
            average_faithfulness_score=(
                average_faithfulness_score
            ),
            average_answer_relevance_score=(
                average_answer_relevance_score
            ),
            average_answer_correctness_score=(
                average_answer_correctness_score
            ),
            average_overall_score=(
                average_overall_score
            ),
            hallucination_count=(
                hallucination_count
            ),
            hallucination_rate=(
                hallucination_rate
            ),
            passed_count=passed_count,
            failed_count=failed_count,
            pass_rate=pass_rate,
            generated_at=(
                generated_at
                or datetime.now(UTC)
            ),
            interpretation=interpretation,
            notes=notes,
        )