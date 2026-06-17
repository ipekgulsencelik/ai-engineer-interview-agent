from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from src.evaluation.runner.validators.runner_execution_result_validator import (
    RunnerExecutionResultValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class RunnerExecutionResult:
    """
    Immutable runner execution result.

    Represents the outcome of a single runner
    execution for scheduled reports, BI exports,
    telemetry exports, dashboard refreshes,
    artifact delivery, distributed jobs, and
    background workflows.
    """

    execution_id: str

    runner_id: str

    runner_name: str

    status: str

    started_at: datetime

    completed_at: datetime | None = None

    duration_ms: float | None = None

    success: bool = False

    score: float | None = None

    error_message: str | None = None

    retry_count: int = 0

    output_uri: str | None = None

    artifact_id: str | None = None

    report_id: str | None = None

    dataset_id: str | None = None

    run_id: str | None = None

    experiment_id: str | None = None

    worker_id: str | None = None

    correlation_id: str | None = None

    trace_id: str | None = None

    metadata: dict[
        str,
        str,
    ] | None = None

    def __post_init__(
        self,
    ) -> None:
        RunnerExecutionResultValidator.validate(
            execution_id=self.execution_id,
            runner_id=self.runner_id,
            runner_name=self.runner_name,
            status=self.status,
            started_at=self.started_at,
            completed_at=self.completed_at,
            duration_ms=self.duration_ms,
            success=self.success,
            score=self.score,
            error_message=self.error_message,
            retry_count=self.retry_count,
            output_uri=self.output_uri,
            artifact_id=self.artifact_id,
            report_id=self.report_id,
            dataset_id=self.dataset_id,
            run_id=self.run_id,
            experiment_id=self.experiment_id,
            worker_id=self.worker_id,
            correlation_id=self.correlation_id,
            trace_id=self.trace_id,
            metadata=self.metadata,
        )

    @property
    def is_completed(
        self,
    ) -> bool:
        return (
            self.completed_at
            is not None
        )

    @property
    def is_successful(
        self,
    ) -> bool:
        return self.success

    @property
    def is_failed(
        self,
    ) -> bool:
        return not self.success

    @property
    def has_score(
        self,
    ) -> bool:
        return (
            self.score
            is not None
        )

    @property
    def has_error(
        self,
    ) -> bool:
        return (
            self.error_message
            is not None
        )

    @property
    def was_retried(
        self,
    ) -> bool:
        return (
            self.retry_count > 0
        )

    @property
    def has_output(
        self,
    ) -> bool:
        return (
            self.output_uri
            is not None
        )

    @property
    def has_artifact(
        self,
    ) -> bool:
        return (
            self.artifact_id
            is not None
        )

    @property
    def has_report(
        self,
    ) -> bool:
        return (
            self.report_id
            is not None
        )

    @property
    def has_dataset(
        self,
    ) -> bool:
        return (
            self.dataset_id
            is not None
        )

    @property
    def has_run(
        self,
    ) -> bool:
        return (
            self.run_id
            is not None
        )

    @property
    def has_experiment(
        self,
    ) -> bool:
        return (
            self.experiment_id
            is not None
        )

    @property
    def has_worker(
        self,
    ) -> bool:
        return (
            self.worker_id
            is not None
        )

    @property
    def has_trace(
        self,
    ) -> bool:
        return (
            self.trace_id
            is not None
        )

    @property
    def has_metadata(
        self,
    ) -> bool:
        return bool(
            self.metadata,
        )