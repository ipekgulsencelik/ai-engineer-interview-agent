from __future__ import annotations

from datetime import datetime

from src.evaluation.reporting.entities.scheduled_report import (
    ScheduledReport,
)


class ScheduledReportDueChecker:
    """
    Checks whether scheduled reports are due for execution.
    """

    def is_due(
        self,
        *,
        scheduled_report: ScheduledReport,
        now: datetime,
    ) -> bool:
        if not scheduled_report.enabled:
            return False

        if scheduled_report.next_run_at is None:
            return False

        return now >= scheduled_report.next_run_at