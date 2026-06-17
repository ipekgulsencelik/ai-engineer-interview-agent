from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from src.evaluation.reporting.validators.scheduled_report_validator import (
    ScheduledReportValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ScheduledReport:
    """
    Immutable scheduled report definition.

    Represents a recurring report generation job
    for dashboards, benchmarks, experiments,
    executive summaries, trend reports, and
    comparison reports.
    """

    schedule_id: str

    report_id: str

    report_name: str

    report_type: str

    report_format: str

    cron_expression: str

    output_directory: str

    created_at: datetime

    enabled: bool = True

    dashboard_id: str | None = None

    experiment_id: str | None = None

    run_id: str | None = None

    benchmark_id: str | None = None

    model_name: str | None = None

    generated_by: str | None = None

    last_run_at: datetime | None = None

    next_run_at: datetime | None = None

    execution_count: int = 0

    failure_count: int = 0

    last_error: str | None = None

    recipient_emails: tuple[
        str,
        ...,
    ] = ()

    metadata: dict[
        str,
        str,
    ] | None = None

    notes: str | None = None

    def __post_init__(
        self,
    ) -> None:
        ScheduledReportValidator.validate(
            schedule_id=self.schedule_id,
            report_id=self.report_id,
            report_name=self.report_name,
            report_type=self.report_type,
            report_format=self.report_format,
            cron_expression=self.cron_expression,
            output_directory=self.output_directory,
            created_at=self.created_at,
            enabled=self.enabled,
            dashboard_id=self.dashboard_id,
            experiment_id=self.experiment_id,
            run_id=self.run_id,
            benchmark_id=self.benchmark_id,
            model_name=self.model_name,
            generated_by=self.generated_by,
            last_run_at=self.last_run_at,
            next_run_at=self.next_run_at,
            execution_count=self.execution_count,
            failure_count=self.failure_count,
            last_error=self.last_error,
            recipient_emails=self.recipient_emails,
            metadata=self.metadata,
            notes=self.notes,
        )

    @property
    def has_dashboard(
        self,
    ) -> bool:
        return (
            self.dashboard_id
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
    def has_run(
        self,
    ) -> bool:
        return (
            self.run_id
            is not None
        )

    @property
    def has_benchmark(
        self,
    ) -> bool:
        return (
            self.benchmark_id
            is not None
        )

    @property
    def has_model(
        self,
    ) -> bool:
        return (
            self.model_name
            is not None
        )

    @property
    def has_recipients(
        self,
    ) -> bool:
        return bool(
            self.recipient_emails,
        )

    @property
    def has_metadata(
        self,
    ) -> bool:
        return bool(
            self.metadata,
        )

    @property
    def has_error(
        self,
    ) -> bool:
        return (
            self.last_error
            is not None
        )

    @property
    def success_count(
        self,
    ) -> int:
        return (
            self.execution_count
            - self.failure_count
        )

    @property
    def success_rate(
        self,
    ) -> float:
        if self.execution_count == 0:
            return 1.0

        return (
            self.success_count
            / self.execution_count
        )

    @property
    def is_due(
        self,
    ) -> bool:
        if not self.enabled:
            return False

        if self.next_run_at is None:
            return False

        return (
            datetime.utcnow()
            >= self.next_run_at
        )

    @property
    def never_executed(
        self,
    ) -> bool:
        return (
            self.execution_count == 0
        )

    @property
    def is_failing(
        self,
    ) -> bool:
        return (
            self.failure_count > 0
        )

    @property
    def is_healthy(
        self,
    ) -> bool:
        return (
            self.success_rate >= 0.95
        )