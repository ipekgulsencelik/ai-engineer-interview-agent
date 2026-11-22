from __future__ import annotations

from dataclasses import replace
from datetime import datetime

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)

from src.evaluation.reporting.entities.schedule_report import (
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
            next_run_at=self._pending_next_run(scheduled_report, now),
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
            next_run_at=self._pending_next_run(scheduled_report, now),
        )

        self._store.update(
            scheduled_report=failed_schedule,
        )

        return failed_schedule
    @staticmethod
    def _pending_next_run(
        scheduled_report: ScheduledReport,
        now: datetime,
    ) -> datetime | None:
        """Never persist an elapsed deadline as a future execution time.

        No cron calculation occurs here: the scheduling policy must provide
        the next upcoming run separately before another execution.
        """
        next_run = scheduled_report.next_run_at
        if next_run is None:
            return None

        try:
            return next_run if next_run > now else None
        except TypeError as exc:
            raise EvaluationValidationError(
                "next_run_at and now must have compatible time zones."
            ) from exc
