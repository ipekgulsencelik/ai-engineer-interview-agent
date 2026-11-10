"""Business-safe telemetry instrumentation and failure isolation tests."""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from datetime import UTC, datetime

import pytest

from src.evaluation.dataset.observability.coordinator import (
    DatasetObservabilityCoordinator,
)
from src.evaluation.dataset.observability.delivery import (
    AlertFailureOutcome,
    AlertLease,
    LeasedDatasetAlertDispatcher,
)
from src.evaluation.dataset.observability.models import (
    AlertSeverity,
    MonitoringAlert,
    MonitoringPolicy,
    MonitoringSnapshot,
    MonitoringStatus,
)
from src.evaluation.dataset.observability.telemetry import (
    SafeDatasetTelemetry,
)


def _snapshot(status: MonitoringStatus = MonitoringStatus.HEALTHY) -> MonitoringSnapshot:
    alerts = ()
    if status is MonitoringStatus.WARNING:
        alerts = (
            MonitoringAlert(
                alert_id="private-dataset:alert-1",
                code="DRIFT_WARNING",
                severity=AlertSeverity.WARNING,
                metric="distribution_drift",
                observed=0.2,
                threshold=0.1,
            ),
        )
    return MonitoringSnapshot(
        monitor_run_id="private-dataset:run-1",
        dataset_id="private-dataset",
        dataset_version="2.0.0",
        baseline_dataset_id="private-dataset",
        baseline_dataset_version="1.0.0",
        baseline_quality_run_id="private-baseline",
        comparison_quality_run_id="private-comparison",
        recorded_at=datetime.now(UTC),
        record_count=10,
        baseline_pass_rate=1.0,
        comparison_pass_rate=0.9,
        pass_rate_drop=0.1,
        drift_score=0.2,
        status=status,
        policy=MonitoringPolicy(),
        alerts=alerts,
    )


class _Telemetry:
    def __init__(self, *, fail: bool = False) -> None:
        self.fail = fail
        self.events: list[tuple[object, ...]] = []

    @contextmanager
    def span(self, *, activity: str) -> Iterator[None]:
        self.events.append(("span_enter", activity))
        if self.fail:
            raise RuntimeError("private token in telemetry exception")
        try:
            yield
        finally:
            self.events.append(("span_exit", activity))

    def count(self, *, activity: str, outcome: str, amount: int = 1) -> None:
        self.events.append(("count", activity, outcome, amount))
        if self.fail:
            raise RuntimeError("private token in metrics exception")

    def duration(self, *, activity: str, seconds: float) -> None:
        self.events.append(("duration", activity, seconds))
        if self.fail:
            raise RuntimeError("private token in duration exception")


class _Monitor:
    def __init__(self, snapshot: MonitoringSnapshot, *, fail: bool = False) -> None:
        self.snapshot = snapshot
        self.fail = fail

    def evaluate(self, **kwargs: object) -> MonitoringSnapshot:
        if self.fail:
            raise RuntimeError("business failure: private user data")
        return self.snapshot


class _Store:
    def __init__(self, *, fail: bool = False) -> None:
        self.calls = 0
        self.fail = fail

    def save(self, *, snapshot: MonitoringSnapshot) -> bool:
        self.calls += 1
        if self.fail:
            raise OSError("storage unavailable")
        return True


def _time():
    return iter([100.0, 101.5]).__next__


def test_monitoring_success_uses_bounded_outcome_and_latency() -> None:
    reporter = _Telemetry()
    store = _Store()
    coordinator = DatasetObservabilityCoordinator(
        monitor=_Monitor(_snapshot(MonitoringStatus.WARNING)),
        store=store,
        telemetry=reporter,
        monotonic_clock=_time(),
    )
    result = coordinator.evaluate_and_store(
        baseline_distribution=None,  # fake monitor supplies snapshot
        comparison_distribution=None,
        baseline_quality=None,
        comparison_quality=None,
    )
    assert result.status is MonitoringStatus.WARNING
    assert store.calls == 1
    assert reporter.events == [
        ("span_enter", "monitor"),
        ("count", "monitor", "warning", 1),
        ("duration", "monitor", 1.5),
        ("span_exit", "monitor"),
    ]
    assert "private-dataset" not in repr(reporter.events)


def test_monitoring_failure_is_traced_without_masking_business_error() -> None:
    reporter = _Telemetry()
    coordinator = DatasetObservabilityCoordinator(
        monitor=_Monitor(_snapshot(), fail=True),
        store=_Store(),
        telemetry=reporter,
        monotonic_clock=_time(),
    )
    with pytest.raises(RuntimeError, match="business failure"):
        coordinator.evaluate_and_store(
            baseline_distribution=None,
            comparison_distribution=None,
            baseline_quality=None,
            comparison_quality=None,
        )
    assert ("count", "monitor", "error", 1) in reporter.events
    assert ("duration", "monitor", 1.5) in reporter.events


def test_failed_persistence_is_not_counted_as_successful_monitoring() -> None:
    reporter = _Telemetry()
    coordinator = DatasetObservabilityCoordinator(
        monitor=_Monitor(_snapshot()),
        store=_Store(fail=True),
        telemetry=reporter,
        monotonic_clock=_time(),
    )
    with pytest.raises(OSError, match="storage unavailable"):
        coordinator.evaluate_and_store(
            baseline_distribution=None,
            comparison_distribution=None,
            baseline_quality=None,
            comparison_quality=None,
        )
    assert ("count", "monitor", "error", 1) in reporter.events
    assert not any(
        item[:2] == ("count", "monitor") and item[2] == "healthy"
        for item in reporter.events
    )


def test_telemetry_backend_failure_never_invalidates_committed_result(
    caplog: pytest.LogCaptureFixture,
) -> None:
    reporter = _Telemetry(fail=True)
    coordinator = DatasetObservabilityCoordinator(
        monitor=_Monitor(_snapshot()),
        store=_Store(),
        telemetry=reporter,
        monotonic_clock=_time(),
    )
    result = coordinator.evaluate_and_store(
        baseline_distribution=None,
        comparison_distribution=None,
        baseline_quality=None,
        comparison_quality=None,
    )
    assert result.status is MonitoringStatus.HEALTHY
    assert "private token" not in caplog.text
    assert "telemetry exporter unavailable" in caplog.text


def test_safe_telemetry_noop_never_requires_sdk() -> None:
    reporter = SafeDatasetTelemetry()
    with reporter.span(activity="monitor"):
        reporter.count(activity="monitor", outcome="healthy")
        reporter.duration(activity="monitor", seconds=0.0)


class _Sender:
    def __init__(self, *, fail: bool = False) -> None:
        self.fail = fail
        self.sent = 0

    def send(self, *, alert: MonitoringAlert) -> None:
        self.sent += 1
        if self.fail:
            raise RuntimeError("private user value")


class _Outbox:
    def __init__(self, *, fail: bool = False, dead_letter: bool = False) -> None:
        self.fail_claim = fail
        self.dead_letter = dead_letter
        self.acks = 0
        self.failures = 0
        self.alert = MonitoringAlert(
            alert_id="private-dataset:alert",
            code="DRIFT_WARNING",
            severity=AlertSeverity.WARNING,
            metric="distribution_drift",
            observed=0.2,
            threshold=0.1,
        )

    def claim(self, *, worker_id: str, limit: int, lease_seconds: int):
        if self.fail_claim:
            raise OSError("database unavailable")
        return (
            AlertLease(
                alert=self.alert,
                token="private-token",
                worker_id=worker_id,
                attempt=1,
                expires_at=datetime.now(UTC),
            ),
        )

    def acknowledge(self, *, lease: AlertLease) -> bool:
        self.acks += 1
        return True

    def fail(self, *, lease: AlertLease, reason_code: str) -> AlertFailureOutcome:
        self.failures += 1
        return AlertFailureOutcome(
            alert_id=lease.alert.alert_id,
            attempt=lease.attempt,
            dead_lettered=self.dead_letter,
        )


@pytest.mark.parametrize(
    ("sender_fails", "dead_letter", "outcome"),
    [
        (False, False, "delivered"),
        (True, False, "retry"),
        (True, True, "dead_letter"),
    ],
)
def test_dispatch_records_only_bounded_outcome(
    sender_fails: bool, dead_letter: bool, outcome: str
) -> None:
    reporter = _Telemetry()
    outbox = _Outbox(dead_letter=dead_letter)
    dispatcher = LeasedDatasetAlertDispatcher(
        outbox=outbox,
        sender=_Sender(fail=sender_fails),
        worker_id="secret-worker-name",
        telemetry=reporter,
        monotonic_clock=_time(),
    )
    result = dispatcher.dispatch_once(limit=1)
    assert result.claimed == 1
    assert ("count", "dispatch", outcome, 1) in reporter.events
    assert ("duration", "dispatch", 1.5) in reporter.events
    assert "private-token" not in repr(reporter.events)
    assert "secret-worker" not in repr(reporter.events)


def test_dispatch_failure_counted_without_leaking_database_error() -> None:
    reporter = _Telemetry()
    dispatcher = LeasedDatasetAlertDispatcher(
        outbox=_Outbox(fail=True),
        sender=_Sender(),
        worker_id="worker",
        telemetry=reporter,
        monotonic_clock=_time(),
    )
    with pytest.raises(OSError, match="database unavailable"):
        dispatcher.dispatch_once()
    assert ("count", "dispatch", "error", 1) in reporter.events
    assert ("duration", "dispatch", 1.5) in reporter.events


def test_failed_exporter_does_not_interrupt_alert_receipt() -> None:
    outbox = _Outbox()
    reporter = _Telemetry(fail=True)
    dispatcher = LeasedDatasetAlertDispatcher(
        outbox=outbox,
        sender=_Sender(),
        worker_id="worker",
        telemetry=reporter,
        monotonic_clock=_time(),
    )
    assert dispatcher.dispatch_once().delivered == 1
    assert outbox.acks == 1
