from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime

from src.evaluation.reporting.entities.executive_summary import (
    ExecutiveSummary,
)
from src.evaluation.reporting.entities.report_artifact import (
    ReportArtifact,
)
from src.evaluation.reporting.entities.schedule_report import (
    ScheduledReport,
)
from src.evaluation.reporting.schedulers.scheduled_report_due_checker import (
    ScheduledReportDueChecker,
)
from src.evaluation.reporting.services.scheduled_report_runner import (
    ScheduledReportRunner,
)
from src.evaluation.reporting.utc_datetime import as_utc
from src.evaluation.reporting.stores.scheduled_report_store import (
    ScheduledReportStore,
)


class ReportScheduler:
    """
    Coordinates scheduled report execution.
    """

    def __init__(
        self,
        *,
        store: ScheduledReportStore,
        due_checker: ScheduledReportDueChecker,
        runner: ScheduledReportRunner,
    ) -> None:
        self._store = store
        self._due_checker = due_checker
        self._runner = runner

    def run_due_reports(
        self,
        *,
        summaries: dict[
            str,
            ExecutiveSummary,
        ],
        now: datetime | None = None,
    ) -> tuple[
        ReportArtifact,
        ...,
    ]:
        current_time = as_utc(now if now is not None else datetime.now(UTC))

        artifacts: list[
            ReportArtifact
        ] = []

        for stored_schedule in self._store.list_enabled():
            scheduled_report = self._normalize_schedule(stored_schedule)
            if not self._due_checker.is_due(
                scheduled_report=scheduled_report,
                now=current_time,
            ):
                continue

            artifact = self._runner.run(
                scheduled_report=scheduled_report,
                summaries=summaries,
                now=current_time,
            )

            artifacts.append(
                artifact,
            )

        return tuple(
            artifacts,
        )

    def run_once(
        self,
        *,
        scheduled_report: ScheduledReport,
        summaries: dict[
            str,
            ExecutiveSummary,
        ],
        now: datetime | None = None,
    ) -> ReportArtifact:
        return self._runner.run(
            scheduled_report=self._normalize_schedule(scheduled_report),
            summaries=summaries,
            now=as_utc(now if now is not None else datetime.now(UTC)),
        )

    @staticmethod
    def _normalize_schedule(schedule: ScheduledReport) -> ScheduledReport:
        """Give downstream runners a consistent UTC-aware state snapshot."""
        return replace(
            schedule,
            created_at=as_utc(schedule.created_at),
            last_run_at=(
                as_utc(schedule.last_run_at)
                if schedule.last_run_at is not None
                else None
            ),
            next_run_at=(
                as_utc(schedule.next_run_at)
                if schedule.next_run_at is not None
                else None
            ),
        )