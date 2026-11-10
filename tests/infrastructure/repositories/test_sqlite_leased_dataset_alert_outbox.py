"""Operational tests for fencing, multi-worker claims, backoff, and DLQ."""

from __future__ import annotations

import sqlite3
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from datetime import UTC, datetime, timedelta

import pytest

from src.evaluation.dataset.observability import (
    AlertLeaseError,
    AlertRetryPolicy,
    LeasedDatasetAlertDispatcher,
    MonitoringAlert,
    MonitoringPolicy,
    MonitoringSnapshot,
    MonitoringStatus,
    AlertSeverity,
    ObservabilityStorageError,
)
from src.infrastructure.repositories.sqlite_dataset_observability_repository import (
    SQLiteDatasetObservabilityRepository,
)
from src.infrastructure.repositories.sqlite_leased_dataset_alert_outbox import (
    SQLiteLeasedDatasetAlertOutbox,
)


class FixedClock:
    def __init__(self) -> None:
        self.value = datetime(2026, 11, 10, 12, tzinfo=UTC)

    def now(self) -> datetime:
        return self.value

    def advance(self, seconds: int) -> None:
        self.value += timedelta(seconds=seconds)


def make_snapshot(number: int = 0) -> MonitoringSnapshot:
    run_id = f"monitor-{number}"
    return MonitoringSnapshot(
        monitor_run_id=run_id,
        dataset_id="dataset",
        dataset_version="2.0.0",
        baseline_dataset_id="dataset",
        baseline_dataset_version="1.0.0",
        baseline_quality_run_id=f"baseline-{number}",
        comparison_quality_run_id=f"comparison-{number}",
        recorded_at=datetime(2026, 11, 10, 12, tzinfo=UTC),
        record_count=10,
        baseline_pass_rate=1.0,
        comparison_pass_rate=0.9,
        pass_rate_drop=0.1,
        drift_score=0.2,
        status=MonitoringStatus.WARNING,
        policy=MonitoringPolicy(),
        alerts=(
            MonitoringAlert(
                alert_id=f"{run_id}:DRIFT_WARNING",
                code="DRIFT_WARNING",
                severity=AlertSeverity.WARNING,
                metric="distribution_drift",
                observed=0.2,
                threshold=0.1,
            ),
        ),
    )


def make_store(tmp_path, clock=None, policy=None):
    path = tmp_path / "monitor.sqlite"
    base = SQLiteDatasetObservabilityRepository(path)
    outbox = SQLiteLeasedDatasetAlertOutbox(
        path, clock=clock, policy=policy,
    )
    return base, outbox, path


def test_existing_outbox_is_migrated_without_losing_alerts(tmp_path) -> None:
    path = tmp_path / "monitor.sqlite"
    original = SQLiteDatasetObservabilityRepository(path)
    snapshot = make_snapshot()
    original.save(snapshot=snapshot)
    clock = FixedClock()

    store = SQLiteLeasedDatasetAlertOutbox(path, clock=clock)
    leases = store.claim(worker_id="worker-1", limit=10, lease_seconds=30)
    assert len(leases) == 1
    assert leases[0].alert == snapshot.alerts[0]
    assert leases[0].attempt == 1
    assert store.acknowledge(lease=leases[0])
    assert store.claim(worker_id="worker-2", limit=10, lease_seconds=30) == ()
    assert store.delivery_events(alert_id=snapshot.alerts[0].alert_id) == (
        ("claimed", 1, None),
        ("delivered", 1, None),
    )

    reopened = SQLiteLeasedDatasetAlertOutbox(path, clock=clock)
    assert reopened.dead_letters() == ()
    assert reopened.claim(worker_id="worker-3", limit=10, lease_seconds=30) == ()
    assert original.get(monitor_run_id=snapshot.monitor_run_id) == snapshot
    with sqlite3.connect(path) as conn:
        count = conn.execute(
            "SELECT COUNT(*) FROM dataset_monitor_alert_receipts"
        ).fetchone()[0]
    assert count == 1


def test_legacy_dispatch_cannot_bypass_leases_after_schema_upgrade(tmp_path) -> None:
    old, store, _path = make_store(tmp_path)
    old.save(snapshot=make_snapshot())
    with pytest.raises(ObservabilityStorageError, match="legacy alert delivery"):
        old.pending()
    with pytest.raises(ObservabilityStorageError, match="legacy alert delivery"):
        old.mark_delivered(alert_id="monitor-0:DRIFT_WARNING")
    assert len(store.claim(worker_id="new", limit=1, lease_seconds=10)) == 1


def test_concurrent_workers_claim_distinct_alerts(tmp_path) -> None:
    old, _store, path = make_store(tmp_path)
    for idx in range(12):
        old.save(snapshot=make_snapshot(idx))
    clock = FixedClock()

    def attempt(worker: int):
        return SQLiteLeasedDatasetAlertOutbox(path, clock=clock).claim(
            worker_id=f"worker-{worker}", limit=4, lease_seconds=60
        )

    with ThreadPoolExecutor(max_workers=6) as pool:
        groups = list(pool.map(attempt, range(6)))
    claims = [lease for group in groups for lease in group]
    assert len(claims) == 12
    assert len({lease.alert.alert_id for lease in claims}) == 12
    assert len({lease.token for lease in claims}) == 12
    for lease in claims:
        assert SQLiteLeasedDatasetAlertOutbox(path, clock=clock).acknowledge(
            lease=lease
        )


def test_expired_lease_requires_backoff_then_reclaims_with_new_token(
    tmp_path,
) -> None:
    clock = FixedClock()
    old, store, _path = make_store(
        tmp_path, clock=clock,
        policy=AlertRetryPolicy(
            max_attempts=3,
            initial_delay_seconds=10,
            max_delay_seconds=25,
        ),
    )
    old.save(snapshot=make_snapshot())
    initial = store.claim(worker_id="w1", limit=1, lease_seconds=5)[0]
    clock.advance(5)
    assert store.claim(worker_id="w2", limit=1, lease_seconds=5) == ()
    with pytest.raises(AlertLeaseError, match="expired"):
        store.acknowledge(lease=initial)
    assert store.delivery_events(alert_id=initial.alert.alert_id)[-1] == (
        "lease_expired", 1, "LEASE_EXPIRED",
    )
    clock.advance(10)
    replacement = store.claim(worker_id="w2", limit=1, lease_seconds=5)[0]
    assert replacement.attempt == 2
    assert replacement.token != initial.token
    with pytest.raises(AlertLeaseError, match="ownership"):
        store.fail(lease=initial, reason_code="SENDER_FAILURE")
    assert store.acknowledge(lease=replacement)


def test_exponential_backoff_and_dead_letter_after_bounded_attempts(
    tmp_path,
) -> None:
    clock = FixedClock()
    old, store, _ = make_store(
        tmp_path,
        clock=clock,
        policy=AlertRetryPolicy(
            max_attempts=3, initial_delay_seconds=10, max_delay_seconds=15
        ),
    )
    old.save(snapshot=make_snapshot())
    for attempt in range(1, 4):
        lease = store.claim(
            worker_id="worker", limit=1, lease_seconds=30
        )[0]
        assert lease.attempt == attempt
        outcome = store.fail(lease=lease, reason_code="SENDER_FAILURE")
        assert outcome.dead_lettered is (attempt == 3)
        assert store.claim(worker_id="other", limit=1, lease_seconds=30) == ()
        if attempt != 3:
            clock.advance(10 if attempt == 1 else 15)
    assert store.dead_letters() == make_snapshot().alerts
    assert store.delivery_events(alert_id=lease.alert.alert_id) == (
        ("claimed", 1, None),
        ("retry", 1, "SENDER_FAILURE"),
        ("claimed", 2, None),
        ("retry", 2, "SENDER_FAILURE"),
        ("claimed", 3, None),
        ("dead_letter", 3, "SENDER_FAILURE"),
    )


def test_exhausted_crash_is_dead_lettered_after_lease_expiration(
    tmp_path,
) -> None:
    clock = FixedClock()
    old, store, _path = make_store(
        tmp_path, clock=clock,
        policy=AlertRetryPolicy(max_attempts=1),
    )
    old.save(snapshot=make_snapshot())
    lease = store.claim(worker_id="w1", limit=1, lease_seconds=1)[0]
    clock.advance(1)
    assert store.claim(worker_id="w2", limit=1, lease_seconds=1) == ()
    assert store.dead_letters() == make_snapshot().alerts
    assert store.delivery_events(alert_id=lease.alert.alert_id)[-1] == (
        "dead_letter", 1, "LEASE_EXPIRED",
    )


def test_manual_dead_letter_requeue_requires_operator_action(tmp_path) -> None:
    clock = FixedClock()
    old, store, path = make_store(
        tmp_path,
        clock=clock,
        policy=AlertRetryPolicy(max_attempts=1),
    )
    old.save(snapshot=make_snapshot())
    lease = store.claim(worker_id="worker", limit=1, lease_seconds=10)[0]
    assert store.fail(lease=lease, reason_code="SENDER_FAILURE").dead_lettered
    assert store.requeue(alert_id=lease.alert.alert_id)
    assert not store.requeue(alert_id=lease.alert.alert_id)
    assert store.dead_letters() == ()
    new_store = SQLiteLeasedDatasetAlertOutbox(
        path, clock=clock, policy=AlertRetryPolicy(max_attempts=1)
    )
    second = new_store.claim(worker_id="worker", limit=1, lease_seconds=10)[0]
    assert second.attempt == 1
    assert new_store.acknowledge(lease=second)
    with pytest.raises(AlertLeaseError, match="already delivered"):
        new_store.requeue(alert_id=lease.alert.alert_id)
    assert ("requeued", 0, None) in new_store.delivery_events(
        alert_id=lease.alert.alert_id
    )


def test_acknowledgment_fault_rolls_back_delivery_and_receipt(tmp_path) -> None:
    clock = FixedClock()
    old, store, path = make_store(tmp_path, clock=clock)
    old.save(snapshot=make_snapshot())
    lease = store.claim(worker_id="w", limit=1, lease_seconds=30)[0]
    with sqlite3.connect(path) as conn:
        conn.execute(
            """
            CREATE TRIGGER block_receipt BEFORE INSERT
            ON dataset_monitor_alert_receipts
            BEGIN SELECT RAISE(ABORT, 'fault injection'); END
            """
        )
    with pytest.raises(ObservabilityStorageError, match="receipt transaction"):
        store.acknowledge(lease=lease)
    assert len(store.delivery_events(alert_id=lease.alert.alert_id)) == 1
    assert store.claim(worker_id="other", limit=1, lease_seconds=30) == ()
    with sqlite3.connect(path) as conn:
        conn.execute("DROP TRIGGER block_receipt")
    assert store.acknowledge(lease=lease)


def test_claim_audit_failure_does_not_grant_lease(tmp_path) -> None:
    clock = FixedClock()
    old, store, path = make_store(tmp_path, clock=clock)
    old.save(snapshot=make_snapshot())
    with sqlite3.connect(path) as conn:
        conn.execute(
            """
            CREATE TRIGGER block_claim BEFORE INSERT
            ON dataset_monitor_alert_delivery_events
            BEGIN SELECT RAISE(ABORT, 'injected failure'); END
            """
        )
    with pytest.raises(ObservabilityStorageError, match="claim failed"):
        store.claim(worker_id="w", limit=1, lease_seconds=30)
    with sqlite3.connect(path) as conn:
        conn.execute("DROP TRIGGER block_claim")
    lease = store.claim(worker_id="w", limit=1, lease_seconds=30)[0]
    assert lease.attempt == 1


def test_invalid_reason_code_and_leased_claims_fail_closed(tmp_path) -> None:
    clock = FixedClock()
    old, store, _ = make_store(tmp_path, clock=clock)
    old.save(snapshot=make_snapshot())
    lease = store.claim(worker_id="worker", limit=1, lease_seconds=30)[0]
    with pytest.raises(ValueError, match="stable uppercase"):
        store.fail(lease=lease, reason_code="candidate=private answer")
    with pytest.raises(AlertLeaseError, match="ownership"):
        store.acknowledge(lease=replace(lease, token="fake"))
    assert store.acknowledge(lease=lease)


class Sender:
    def __init__(self, *, fail: bool) -> None:
        self.fail = fail
        self.sent: list[str] = []

    def send(self, *, alert: MonitoringAlert) -> None:
        if self.fail:
            raise RuntimeError("private candidate data leaked in exception")
        self.sent.append(alert.alert_id)


def test_dispatcher_schedules_failure_without_storing_exception_text(
    tmp_path,
) -> None:
    clock = FixedClock()
    old, store, path = make_store(
        tmp_path, clock=clock,
        policy=AlertRetryPolicy(max_attempts=2, initial_delay_seconds=10),
    )
    old.save(snapshot=make_snapshot())
    sender = Sender(fail=True)
    dispatcher = LeasedDatasetAlertDispatcher(
        outbox=store, sender=sender, worker_id="worker", lease_seconds=30
    )
    first = dispatcher.dispatch_once(limit=10)
    assert (first.claimed, first.delivered, first.retry_scheduled, first.dead_lettered) == (
        1, 0, 1, 0
    )
    assert b"private candidate data leaked" not in path.read_bytes()
    clock.advance(10)
    sender.fail = False
    result = dispatcher.dispatch_once()
    assert (result.claimed, result.delivered) == (1, 1)
    assert sender.sent == ["monitor-0:DRIFT_WARNING"]
    assert dispatcher.dispatch_once().claimed == 0


def test_delivery_persistence_survives_restart_and_is_idempotent(tmp_path) -> None:
    clock = FixedClock()
    old, store, path = make_store(tmp_path, clock=clock)
    old.save(snapshot=make_snapshot())
    lease = store.claim(worker_id="w1", limit=1, lease_seconds=30)[0]
    reopened = SQLiteLeasedDatasetAlertOutbox(path, clock=clock)
    assert reopened.claim(worker_id="w2", limit=1, lease_seconds=30) == ()
    assert reopened.acknowledge(lease=lease)
    with pytest.raises(AlertLeaseError):
        store.acknowledge(lease=lease)
    assert reopened.delivery_events(alert_id=lease.alert.alert_id)[-1][0] == (
        "delivered"
    )


def test_invalid_settings_and_bounds_are_rejected(tmp_path) -> None:
    for policy_values in (
        {"max_attempts": True},
        {"max_attempts": 0},
        {"initial_delay_seconds": 0},
        {"max_delay_seconds": 5, "initial_delay_seconds": 10},
    ):
        with pytest.raises(ValueError):
            AlertRetryPolicy(**policy_values)
    _old, store, _path = make_store(tmp_path)
    for kwargs in (
        {"worker_id": "", "limit": 1, "lease_seconds": 1},
        {"worker_id": "w", "limit": 0, "lease_seconds": 1},
        {"worker_id": "w", "limit": True, "lease_seconds": 1},
        {"worker_id": "w", "limit": 1, "lease_seconds": 0},
    ):
        with pytest.raises(ValueError):
            store.claim(**kwargs)
    with pytest.raises(ValueError):
        store.dead_letters(limit=0)


def test_delivery_events_do_not_contain_sample_payload(tmp_path) -> None:
    old, store, path = make_store(tmp_path)
    old.save(snapshot=make_snapshot())
    lease = store.claim(worker_id="worker", limit=1, lease_seconds=60)[0]
    store.fail(lease=lease, reason_code="SENDER_FAILURE")
    assert b"candidate answer private" not in path.read_bytes()
    assert all(
        code in (None, "SENDER_FAILURE")
        for _event, _attempt, code in store.delivery_events(
            alert_id=lease.alert.alert_id
        )
    )
