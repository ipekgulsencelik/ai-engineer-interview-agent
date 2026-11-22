"""Real scheduler state transitions with a replaceable storage adapter."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from unittest.mock import Mock

from src.evaluation.reporting.entities.schedule_report import ScheduledReport
from src.evaluation.reporting.schedulers.report_scheduler import ReportScheduler
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


def test_elapsed_run_deadline_is_cleared_after_success_and_failure() -> None:
    """An overdue schedule must not repeatedly execute or fail validation."""
    due = datetime(2026, 11, 22, tzinfo=UTC)
    store = MemoryScheduledReportStore(_schedule(due))
    service = ScheduledReportStateService(store=store)
    executed_at = due + timedelta(minutes=4)
    complete = service.mark_success(
        scheduled_report=store.schedule,
        now=executed_at,
    )
    assert complete.last_run_at == executed_at
    assert complete.next_run_at is None
    assert not complete.is_due

    failed = service.mark_failure(
        scheduled_report=complete,
        now=executed_at + timedelta(minutes=2),
        error="Downstream export unavailable",
    )
    assert failed.next_run_at is None
    assert failed.failure_count == 1
    assert failed.execution_count == 2


def test_future_run_deadline_remains_when_executed_early() -> None:
    due = datetime(2026, 11, 22, tzinfo=UTC)
    store = MemoryScheduledReportStore(_schedule(due))
    result = ScheduledReportStateService(store=store).mark_success(
        scheduled_report=store.schedule,
        now=due - timedelta(seconds=30),
    )
    assert result.next_run_at == due


def test_schedule_is_due_supports_aware_and_legacy_utc_naive_values() -> None:
    from dataclasses import replace

    past = datetime(2000, 1, 1, tzinfo=UTC)
    future = datetime(2999, 1, 1, tzinfo=UTC)
    schedule = _schedule(past)
    assert schedule.is_due
    assert not replace(schedule, next_run_at=future).is_due
    assert replace(schedule, next_run_at=past.replace(tzinfo=None)).is_due
    assert not replace(
        schedule,
        next_run_at=future.replace(tzinfo=None),
    ).is_due


def test_due_reports_normalizes_legacy_naive_deadline_and_clock() -> None:
    """A legacy UTC-naive schedule must not crash a default-clock batch."""
    from src.evaluation.reporting.services.scheduled_report_runner import (
        ScheduledReportRunner,
    )

    naive_due = datetime(2000, 1, 1)
    store = MemoryScheduledReportStore(_schedule(naive_due))
    runner = Mock(spec=ScheduledReportRunner)
    artifact = object()
    runner.run.return_value = artifact

    scheduler = ReportScheduler(
        store=store,
        due_checker=ScheduledReportDueChecker(),
        runner=runner,
    )
    result = scheduler.run_due_reports(summaries={})
    assert result == (artifact,)
    params = runner.run.call_args.kwargs
    assert params["now"].tzinfo == UTC
    assert params["scheduled_report"].created_at.tzinfo == UTC
    assert params["scheduled_report"].next_run_at.tzinfo == UTC

    # State updates consume the UTC-aware arguments passed to the runner.
    updated = ScheduledReportStateService(store=store).mark_success(
        scheduled_report=params["scheduled_report"],
        now=params["now"],
    )
    assert updated.last_run_at.tzinfo == UTC
    assert updated.next_run_at is None


def test_due_checker_normalizes_explicit_offset_and_naive_dates() -> None:
    from datetime import timezone

    checker = ScheduledReportDueChecker()
    instant = datetime(2026, 11, 23, 12, tzinfo=UTC)
    schedule = _schedule(instant.replace(tzinfo=None))
    assert checker.is_due(scheduled_report=schedule, now=instant)
    assert not checker.is_due(
        scheduled_report=schedule,
        now=instant - timedelta(seconds=1),
    )
    offset = timezone(timedelta(hours=3))
    assert checker.is_due(
        scheduled_report=schedule,
        now=instant.astimezone(offset),
    )
