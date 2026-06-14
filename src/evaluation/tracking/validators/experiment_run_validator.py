from __future__ import annotations

from datetime import datetime

from src.domain.validation.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.tracking.enums.experiment_run_status import (
    ExperimentRunStatus,
)
from src.evaluation.tracking.schemas.experiment_run_schema import (
    EXPERIMENT_RUN_SCHEMA,
)


class ExperimentRunValidator:
    """
    ExperimentRun validation service.
    """

    @staticmethod
    def validate(
        *,
        run_id: str,
        experiment_id: str,
        experiment_name: str,
        experiment_version: str,
        dataset_id: str | None,
        dataset_name: str | None,
        dataset_version: str | None,
        benchmark_id: str | None,
        benchmark_name: str | None,
        benchmark_version: str | None,
        model_name: str | None,
        retriever_name: str | None,
        evaluator_name: str | None,
        overall_score: float | None,
        pass_rate: float | None,
        sample_count: int | None,
        passed_count: int | None,
        failed_count: int | None,
        started_at: datetime,
        completed_at: datetime | None,
        duration_ms: float | None,
        status: ExperimentRunStatus,
        notes: str | None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "run_id": run_id,
                "experiment_id": experiment_id,
                "experiment_name": experiment_name,
                "experiment_version": experiment_version,
                "dataset_id": dataset_id,
                "dataset_name": dataset_name,
                "dataset_version": dataset_version,
                "benchmark_id": benchmark_id,
                "benchmark_name": benchmark_name,
                "benchmark_version": benchmark_version,
                "model_name": model_name,
                "retriever_name": retriever_name,
                "evaluator_name": evaluator_name,
                "overall_score": overall_score,
                "pass_rate": pass_rate,
                "sample_count": sample_count,
                "passed_count": passed_count,
                "failed_count": failed_count,
                "started_at": started_at,
                "completed_at": (
                    completed_at
                    or started_at
                ),
                "duration_ms": duration_ms,
                "status": str(
                    status,
                ),
                "notes": notes,
            },
            schema=EXPERIMENT_RUN_SCHEMA,
            error_factory=EvaluationValidationError,
        )

        if not isinstance(
            status,
            ExperimentRunStatus,
        ):
            raise EvaluationValidationError(
                "status must be ExperimentRunStatus."
            )

        if (
            completed_at is not None
            and completed_at < started_at
        ):
            raise EvaluationValidationError(
                "completed_at cannot be before started_at."
            )

        if (
            passed_count is not None
            and failed_count is not None
            and sample_count is not None
            and passed_count + failed_count != sample_count
        ):
            raise EvaluationValidationError(
                "passed_count + failed_count must equal sample_count."
            )

        if (
            status.is_terminal
            and completed_at is None
        ):
            raise EvaluationValidationError(
                "completed_at is required for terminal experiment runs."
            )

        if (
            status.is_active
            and completed_at is not None
        ):
            raise EvaluationValidationError(
                "completed_at must be empty for active experiment runs."
            )

        if (
            status.is_active
            and duration_ms is not None
        ):
            raise EvaluationValidationError(
                "duration_ms must be empty for active experiment runs."
            )

        if (
            status.is_terminal
            and duration_ms is None
        ):
            raise EvaluationValidationError(
                "duration_ms is required for terminal experiment runs."
            )