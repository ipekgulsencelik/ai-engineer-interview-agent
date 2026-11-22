"""Real scheduler state transitions with a replaceable storage adapter."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

from src.evaluation.reporting.entities.schedule_report import ScheduledReport
from src.evaluation.reporting.schedulers.scheduled_report_due_checker import (
    ScheduledReportDueChecker,
)
from src.evaluation.reporting.services.scheduled_report_state_service import (
    ScheduledReportStateService,
)


class MemoryScheduledReportStore:
    """Test adapter implementing the storage port without database I/O."""

    def __init__(self, schedule: ScheduledReport) -> None:
        self.schedule = schedule

    def list_enabled(self) -> tuple[ScheduledReport, ...]:
        return (self.schedule,) if self.schedule.enabled else ()

    def update(self, *, scheduled_report: ScheduledReport) -> None:
        self.schedule = scheduled_report


def _schedule(now: datetime) -> ScheduledReport:
    return ScheduledReport(
        schedule_id="schedule-001",
        report_id="report-001",
        report_name="Weekly Executive Summary",
        report_type="executive_summary",
        report_format="json",
        cron_expression="0 12 * * MON",
        output_directory="reports",
        created_at=now - timedelta(days=1),
        next_run_at=now,
    )


def test_due_checker_respects_schedule_state_and_clock() -> None:
    now = datetime(2026, 11, 22, tzinfo=UTC)
    checker = ScheduledReportDueChecker()
    schedule = _schedule(now)
    assert checker.is_due(scheduled_report=schedule, now=now)
    assert not checker.is_due(
        scheduled_report=schedule, now=now - timedelta(seconds=1)
    )


def test_store_port_tracks_success_and_failure_without_mutating_previous() -> None:
    now = datetime(2026, 11, 22, tzinfo=UTC)
    initial = _schedule(now)
    store = MemoryScheduledReportStore(initial)
    service = ScheduledReportStateService(store=store)
    success = service.mark_success(scheduled_report=initial, now=now)
    assert initial.execution_count == 0
    assert success.execution_count == 1
    assert success.failure_count == 0
    assert success.last_run_at == now
    assert store.list_enabled() == (success,)

    failed = service.mark_failure(
        scheduled_report=success,
        now=now,
        error="Export failed",
    )
    assert failed.execution_count == 2
    assert failed.failure_count == 1
    assert failed.last_error == "Export failed"
    assert store.schedule is failed
    assert success.last_error is None
