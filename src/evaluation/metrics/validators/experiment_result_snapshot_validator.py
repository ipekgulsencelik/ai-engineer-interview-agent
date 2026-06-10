from __future__ import annotations

from datetime import datetime

from src.domain.validation.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.metrics.reports.benchmark_evaluation_report import (
    BenchmarkEvaluationReport,
)
from src.evaluation.metrics.schemas.experiment_result_snapshot_schema import (
    EXPERIMENT_RESULT_SNAPSHOT_SCHEMA,
)


class ExperimentResultSnapshotValidator:
    """
    ExperimentResultSnapshot validation service.
    """

    @staticmethod
    def validate(
        *,
        experiment_id: str,
        benchmark_id: str,
        benchmark_version: str,
        dataset_id: str,
        dataset_version: str,
        dataset_hash: str,
        model_name: str,
        metrics_version: str,
        benchmark_report: BenchmarkEvaluationReport,
        execution_time_seconds: float,
        created_at: datetime,
        tags: tuple[str, ...],
        notes: str | None = None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "experiment_id": experiment_id,
                "benchmark_id": benchmark_id,
                "benchmark_version": benchmark_version,
                "dataset_id": dataset_id,
                "dataset_version": dataset_version,
                "dataset_hash": dataset_hash,
                "model_name": model_name,
                "metrics_version": metrics_version,
                "execution_time_seconds": execution_time_seconds,
                "tags": tags,
                "notes": notes,
            },
            schema=EXPERIMENT_RESULT_SNAPSHOT_SCHEMA,
            error_factory=EvaluationValidationError,
        )

        ExperimentResultSnapshotValidator._validate_types(
            benchmark_report=benchmark_report,
            created_at=created_at,
        )

    @staticmethod
    def _validate_types(
        *,
        benchmark_report: BenchmarkEvaluationReport,
        created_at: datetime,
    ) -> None:
        if not isinstance(
            benchmark_report,
            BenchmarkEvaluationReport,
        ):
            raise EvaluationValidationError(
                "benchmark_report must be BenchmarkEvaluationReport."
            )

        if not isinstance(
            created_at,
            datetime,
        ):
            raise EvaluationValidationError(
                "created_at must be datetime."
            )