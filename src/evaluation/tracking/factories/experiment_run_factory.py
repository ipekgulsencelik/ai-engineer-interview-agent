from __future__ import annotations

from datetime import UTC
from datetime import datetime
from uuid import uuid4

from src.evaluation.tracking.entities.experiment_run import (
    ExperimentRun,
)
from src.evaluation.tracking.enums.experiment_run_status import (
    ExperimentRunStatus,
)


class ExperimentRunFactory:
    """
    Factory for creating experiment run entities.
    """

    @staticmethod
    def create_pending(
        *,
        experiment_id: str,
        experiment_name: str,
        experiment_version: str,
        dataset_id: str | None = None,
        dataset_name: str | None = None,
        dataset_version: str | None = None,
        benchmark_id: str | None = None,
        benchmark_name: str | None = None,
        benchmark_version: str | None = None,
        model_name: str | None = None,
        retriever_name: str | None = None,
        evaluator_name: str | None = None,
        started_at: datetime | None = None,
        notes: str | None = None,
    ) -> ExperimentRun:
        return ExperimentRun(
            run_id=str(
                uuid4(),
            ),
            experiment_id=experiment_id,
            experiment_name=experiment_name,
            experiment_version=experiment_version,
            dataset_id=dataset_id,
            dataset_name=dataset_name,
            dataset_version=dataset_version,
            benchmark_id=benchmark_id,
            benchmark_name=benchmark_name,
            benchmark_version=benchmark_version,
            model_name=model_name,
            retriever_name=retriever_name,
            evaluator_name=evaluator_name,
            started_at=(
                started_at
                or datetime.now(UTC)
            ),
            status=ExperimentRunStatus.PENDING,
            notes=notes,
        )

    @staticmethod
    def create_running(
        *,
        experiment_id: str,
        experiment_name: str,
        experiment_version: str,
        dataset_id: str | None = None,
        dataset_name: str | None = None,
        dataset_version: str | None = None,
        benchmark_id: str | None = None,
        benchmark_name: str | None = None,
        benchmark_version: str | None = None,
        model_name: str | None = None,
        retriever_name: str | None = None,
        evaluator_name: str | None = None,
        started_at: datetime | None = None,
        notes: str | None = None,
    ) -> ExperimentRun:
        return ExperimentRun(
            run_id=str(
                uuid4(),
            ),
            experiment_id=experiment_id,
            experiment_name=experiment_name,
            experiment_version=experiment_version,
            dataset_id=dataset_id,
            dataset_name=dataset_name,
            dataset_version=dataset_version,
            benchmark_id=benchmark_id,
            benchmark_name=benchmark_name,
            benchmark_version=benchmark_version,
            model_name=model_name,
            retriever_name=retriever_name,
            evaluator_name=evaluator_name,
            started_at=(
                started_at
                or datetime.now(UTC)
            ),
            status=ExperimentRunStatus.RUNNING,
            notes=notes,
        )

    @staticmethod
    def create_completed(
        *,
        experiment_id: str,
        experiment_name: str,
        experiment_version: str,
        started_at: datetime,
        completed_at: datetime | None = None,
        dataset_id: str | None = None,
        dataset_name: str | None = None,
        dataset_version: str | None = None,
        benchmark_id: str | None = None,
        benchmark_name: str | None = None,
        benchmark_version: str | None = None,
        model_name: str | None = None,
        retriever_name: str | None = None,
        evaluator_name: str | None = None,
        overall_score: float | None = None,
        pass_rate: float | None = None,
        sample_count: int | None = None,
        passed_count: int | None = None,
        failed_count: int | None = None,
        notes: str | None = None,
    ) -> ExperimentRun:
        resolved_completed_at = (
            completed_at
            or datetime.now(UTC)
        )

        return ExperimentRun(
            run_id=str(
                uuid4(),
            ),
            experiment_id=experiment_id,
            experiment_name=experiment_name,
            experiment_version=experiment_version,
            dataset_id=dataset_id,
            dataset_name=dataset_name,
            dataset_version=dataset_version,
            benchmark_id=benchmark_id,
            benchmark_name=benchmark_name,
            benchmark_version=benchmark_version,
            model_name=model_name,
            retriever_name=retriever_name,
            evaluator_name=evaluator_name,
            overall_score=overall_score,
            pass_rate=pass_rate,
            sample_count=sample_count,
            passed_count=passed_count,
            failed_count=failed_count,
            started_at=started_at,
            completed_at=resolved_completed_at,
            duration_ms=(
                resolved_completed_at
                - started_at
            ).total_seconds()
            * 1000,
            status=ExperimentRunStatus.COMPLETED,
            notes=notes,
        )

    @staticmethod
    def create_failed(
        *,
        experiment_id: str,
        experiment_name: str,
        experiment_version: str,
        started_at: datetime,
        completed_at: datetime | None = None,
        dataset_id: str | None = None,
        dataset_name: str | None = None,
        dataset_version: str | None = None,
        benchmark_id: str | None = None,
        benchmark_name: str | None = None,
        benchmark_version: str | None = None,
        model_name: str | None = None,
        retriever_name: str | None = None,
        evaluator_name: str | None = None,
        notes: str | None = None,
    ) -> ExperimentRun:
        resolved_completed_at = (
            completed_at
            or datetime.now(UTC)
        )

        return ExperimentRun(
            run_id=str(
                uuid4(),
            ),
            experiment_id=experiment_id,
            experiment_name=experiment_name,
            experiment_version=experiment_version,
            dataset_id=dataset_id,
            dataset_name=dataset_name,
            dataset_version=dataset_version,
            benchmark_id=benchmark_id,
            benchmark_name=benchmark_name,
            benchmark_version=benchmark_version,
            model_name=model_name,
            retriever_name=retriever_name,
            evaluator_name=evaluator_name,
            started_at=started_at,
            completed_at=resolved_completed_at,
            duration_ms=(
                resolved_completed_at
                - started_at
            ).total_seconds()
            * 1000,
            status=ExperimentRunStatus.FAILED,
            notes=notes,
        )