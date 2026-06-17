from __future__ import annotations

from dataclasses import replace
from datetime import datetime

from src.evaluation.reporting.entities.scheduled_report import (
    ScheduledReport,
)
from src.evaluation.reporting.stores.scheduled_report_store import (
    ScheduledReportStore,
)


class ScheduledReportStateService:
    """
    Updates scheduled report execution state.
    """

    def __init__(
        self,
        *,
        store: ScheduledReportStore,
    ) -> None:
        self._store = store

    def mark_success(
        self,
        *,
        scheduled_report: ScheduledReport,
        now: datetime,
    ) -> ScheduledReport:
        updated_schedule = replace(
            scheduled_report,
            execution_count=(
                scheduled_report.execution_count + 1
            ),
            last_run_at=now,
            last_error=None,
        )

        self._store.update(
            scheduled_report=updated_schedule,
        )

        return updated_schedule

    def mark_failure(
        self,
        *,
        scheduled_report: ScheduledReport,
        now: datetime,
        error: str,
    ) -> ScheduledReport:
        failed_schedule = replace(
            scheduled_report,
            execution_count=(
                scheduled_report.execution_count + 1
            ),
            failure_count=(
                scheduled_report.failure_count + 1
            ),
            last_error=error,
            last_run_at=now,
        )

        self._store.update(
            scheduled_report=failed_schedule,
        )

        return failed_schedule