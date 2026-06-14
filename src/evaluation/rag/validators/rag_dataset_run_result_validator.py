from __future__ import annotations

from datetime import datetime

from src.domain.validators.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.rag.entities.rag_evaluation_report import (
    RAGEvaluationReport,
)
from src.evaluation.rag.schemas.rag_dataset_run_result_schema import (
    RAG_DATASET_RUN_RESULT_SCHEMA,
)


class RAGDatasetRunResultValidator:
    """
    RAGDatasetRunResult validation service.
    """

    @staticmethod
    def validate(
        *,
        run_id: str,
        experiment_id: str,
        benchmark_id: str,
        benchmark_name: str,
        benchmark_version: str,
        model_name: str,
        retriever_name: str,
        evaluator_name: str,
        report: RAGEvaluationReport,
        sample_count: int,
        passed_count: int,
        failed_count: int,
        pass_rate: float,
        overall_score: float,
        started_at: datetime,
        completed_at: datetime,
        duration_ms: float,
        interpretation: str,
        notes: str | None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "run_id": run_id,
                "experiment_id": experiment_id,
                "benchmark_id": benchmark_id,
                "benchmark_name": benchmark_name,
                "benchmark_version": benchmark_version,
                "model_name": model_name,
                "retriever_name": retriever_name,
                "evaluator_name": evaluator_name,
                "sample_count": sample_count,
                "passed_count": passed_count,
                "failed_count": failed_count,
                "pass_rate": pass_rate,
                "overall_score": overall_score,
                "started_at": started_at,
                "completed_at": completed_at,
                "duration_ms": duration_ms,
                "interpretation": interpretation,
                "notes": notes,
            },
            schema=RAG_DATASET_RUN_RESULT_SCHEMA,
            error_factory=EvaluationValidationError,
        )

        if not isinstance(
            report,
            RAGEvaluationReport,
        ):
            raise EvaluationValidationError(
                "report must be RAGEvaluationReport."
            )

        if completed_at < started_at:
            raise EvaluationValidationError(
                "completed_at cannot be before started_at."
            )

        if (
            passed_count
            + failed_count
            != sample_count
        ):
            raise EvaluationValidationError(
                "passed_count + failed_count must equal sample_count."
            )

        expected_pass_rate = (
            0.0
            if sample_count == 0
            else passed_count / sample_count
        )

        if abs(
            pass_rate
            - expected_pass_rate,
        ) > 1e-6:
            raise EvaluationValidationError(
                "pass_rate mismatch."
            )

        if sample_count != report.sample_count:
            raise EvaluationValidationError(
                "sample_count must match report.sample_count."
            )

        if passed_count != report.passed_count:
            raise EvaluationValidationError(
                "passed_count must match report.passed_count."
            )

        if failed_count != report.failed_count:
            raise EvaluationValidationError(
                "failed_count must match report.failed_count."
            )

        if abs(
            overall_score
            - report.average_overall_score,
        ) > 1e-6:
            raise EvaluationValidationError(
                "overall_score must match report.average_overall_score."
            )