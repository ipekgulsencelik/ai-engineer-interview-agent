from __future__ import annotations

from dataclasses import replace
from datetime import UTC
from datetime import datetime

from src.evaluation.tracking.entities.experiment_run import (
    ExperimentRun,
)
from src.evaluation.tracking.enums.experiment_run_status import (
    ExperimentRunStatus,
)
from src.evaluation.tracking.factories.experiment_run_factory import (
    ExperimentRunFactory,
)


class ExperimentRunTracker:
    """
    Tracks experiment run lifecycle transitions.

    Produces new immutable ExperimentRun instances
    instead of mutating existing runs.
    """

    def __init__(
        self,
        *,
        run_factory: ExperimentRunFactory | None = None,
    ) -> None:
        self._run_factory = (
            run_factory
            or ExperimentRunFactory()
        )

    def start(
        self,
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
        notes: str | None = None,
    ) -> ExperimentRun:
        return self._run_factory.create_running(
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
            notes=notes,
        )

    def mark_running(
        self,
        *,
        run: ExperimentRun,
    ) -> ExperimentRun:
        self._ensure_not_terminal(
            run=run,
        )

        return replace(
            run,
            status=ExperimentRunStatus.RUNNING,
            completed_at=None,
            duration_ms=None,
        )

    def complete(
        self,
        *,
        run: ExperimentRun,
        overall_score: float,
        pass_rate: float,
        sample_count: int,
        passed_count: int,
        failed_count: int,
        completed_at: datetime | None = None,
        notes: str | None = None,
    ) -> ExperimentRun:
        self._ensure_not_terminal(
            run=run,
        )

        resolved_completed_at = (
            completed_at
            or datetime.now(UTC)
        )

        return replace(
            run,
            overall_score=overall_score,
            pass_rate=pass_rate,
            sample_count=sample_count,
            passed_count=passed_count,
            failed_count=failed_count,
            completed_at=resolved_completed_at,
            duration_ms=(
                resolved_completed_at
                - run.started_at
            ).total_seconds()
            * 1000,
            status=ExperimentRunStatus.COMPLETED,
            notes=(
                notes
                if notes is not None
                else run.notes
            ),
        )

    def fail(
        self,
        *,
        run: ExperimentRun,
        completed_at: datetime | None = None,
        notes: str | None = None,
    ) -> ExperimentRun:
        self._ensure_not_terminal(
            run=run,
        )

        resolved_completed_at = (
            completed_at
            or datetime.now(UTC)
        )

        return replace(
            run,
            completed_at=resolved_completed_at,
            duration_ms=(
                resolved_completed_at
                - run.started_at
            ).total_seconds()
            * 1000,
            status=ExperimentRunStatus.FAILED,
            notes=(
                notes
                if notes is not None
                else run.notes
            ),
        )

    def cancel(
        self,
        *,
        run: ExperimentRun,
        completed_at: datetime | None = None,
        notes: str | None = None,
    ) -> ExperimentRun:
        self._ensure_not_terminal(
            run=run,
        )

        resolved_completed_at = (
            completed_at
            or datetime.now(UTC)
        )

        return replace(
            run,
            completed_at=resolved_completed_at,
            duration_ms=(
                resolved_completed_at
                - run.started_at
            ).total_seconds()
            * 1000,
            status=ExperimentRunStatus.CANCELLED,
            notes=(
                notes
                if notes is not None
                else run.notes
            ),
        )

    def pause(
        self,
        *,
        run: ExperimentRun,
    ) -> ExperimentRun:
        self._ensure_not_terminal(
            run=run,
        )

        return replace(
            run,
            status=ExperimentRunStatus.PAUSED,
            completed_at=None,
            duration_ms=None,
        )

    @staticmethod
    def _ensure_not_terminal(
        *,
        run: ExperimentRun,
    ) -> None:
        if run.status.is_terminal:
            raise ValueError(
                "Terminal experiment runs cannot be modified."
            )