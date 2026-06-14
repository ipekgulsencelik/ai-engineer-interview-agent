from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from src.evaluation.tracking.enums.experiment_run_status import (
    ExperimentRunStatus,
)
from src.evaluation.tracking.validators.experiment_run_validator import (
    ExperimentRunValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ExperimentRun:
    """
    Immutable experiment run.

    Represents a single execution of an experiment
    against a benchmark and dataset configuration.
    """

    run_id: str

    experiment_id: str

    experiment_name: str

    experiment_version: str

    started_at: datetime

    status: ExperimentRunStatus

    dataset_id: str | None = None

    dataset_name: str | None = None

    dataset_version: str | None = None

    benchmark_id: str | None = None

    benchmark_name: str | None = None

    benchmark_version: str | None = None

    model_name: str | None = None

    retriever_name: str | None = None

    evaluator_name: str | None = None

    overall_score: float | None = None

    pass_rate: float | None = None

    sample_count: int | None = None

    passed_count: int | None = None

    failed_count: int | None = None

    completed_at: datetime | None = None

    duration_ms: float | None = None

    notes: str | None = None

    def __post_init__(
        self,
    ) -> None:
        ExperimentRunValidator.validate(
            run_id=self.run_id,
            experiment_id=self.experiment_id,
            experiment_name=self.experiment_name,
            experiment_version=self.experiment_version,
            dataset_id=self.dataset_id,
            dataset_name=self.dataset_name,
            dataset_version=self.dataset_version,
            benchmark_id=self.benchmark_id,
            benchmark_name=self.benchmark_name,
            benchmark_version=self.benchmark_version,
            model_name=self.model_name,
            retriever_name=self.retriever_name,
            evaluator_name=self.evaluator_name,
            overall_score=self.overall_score,
            pass_rate=self.pass_rate,
            sample_count=self.sample_count,
            passed_count=self.passed_count,
            failed_count=self.failed_count,
            started_at=self.started_at,
            completed_at=self.completed_at,
            duration_ms=self.duration_ms,
            status=self.status,
            notes=self.notes,
        )

    @property
    def is_completed(
        self,
    ) -> bool:
        return (
            self.status
            == ExperimentRunStatus.COMPLETED
        )

    @property
    def is_running(
        self,
    ) -> bool:
        return (
            self.status
            == ExperimentRunStatus.RUNNING
        )

    @property
    def is_failed(
        self,
    ) -> bool:
        return (
            self.status
            == ExperimentRunStatus.FAILED
        )

    @property
    def is_cancelled(
        self,
    ) -> bool:
        return (
            self.status
            == ExperimentRunStatus.CANCELLED
        )

    @property
    def is_paused(
        self,
    ) -> bool:
        return (
            self.status
            == ExperimentRunStatus.PAUSED
        )

    @property
    def is_terminal(
        self,
    ) -> bool:
        return self.status.is_terminal

    @property
    def is_active(
        self,
    ) -> bool:
        return self.status.is_active

    @property
    def is_successful(
        self,
    ) -> bool:
        return self.is_completed