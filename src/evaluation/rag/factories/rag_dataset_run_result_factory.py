from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from src.evaluation.rag.entities.rag_evaluation_report import (
    RAGEvaluationReport,
)
from src.evaluation.rag.entities.rag_dataset_run_result import (
    RAGDatasetRunResult,
)


class RAGDatasetRunResultFactory:
    """
    Factory for dataset-level RAG run results.
    """

    @staticmethod
    def create(
        *,
        experiment_id: str,
        model_name: str,
        retriever_name: str,
        evaluator_name: str,
        report: RAGEvaluationReport,
        started_at: datetime,
        completed_at: datetime,
        notes: str | None = None,
    ) -> RAGDatasetRunResult:
        return RAGDatasetRunResult(
            run_id=str(
                uuid4(),
            ),
            experiment_id=experiment_id,
            benchmark_id=report.benchmark_id,
            benchmark_name=report.benchmark_name,
            benchmark_version=report.benchmark_version,
            model_name=model_name,
            retriever_name=retriever_name,
            evaluator_name=evaluator_name,
            report=report,
            sample_count=report.sample_count,
            passed_count=report.passed_count,
            failed_count=report.failed_count,
            pass_rate=report.pass_rate,
            overall_score=report.average_overall_score,
            started_at=started_at,
            completed_at=completed_at,
            duration_ms=(
                completed_at
                - started_at
            ).total_seconds()
            * 1000,
            interpretation=report.interpretation,
            notes=notes,
        )