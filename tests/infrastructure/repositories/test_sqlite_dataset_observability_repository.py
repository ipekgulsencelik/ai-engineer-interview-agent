"""Atomic snapshot/outbox storage, retry, corruption and dispatch tests."""

from __future__ import annotations

import sqlite3
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from datetime import UTC, datetime, timedelta

import pytest

from src.evaluation.dataset.observability import (
    AlertDeliveryError,
    AlertSeverity,
    DatasetAlertDispatcher,
    MonitoringAlert,
    MonitoringPolicy,
    MonitoringSnapshot,
    MonitoringStatus,
    ObservabilityStorageError,
)
from src.infrastructure.repositories.sqlite_dataset_observability_repository import (
    SQLiteDatasetObservabilityRepository,
)


def sample_snapshot() -> MonitoringSnapshot:
    return MonitoringSnapshot(
        monitor_run_id="monitor-1",
        dataset_id="dataset",
        dataset_version="2.0.0",
        baseline_dataset_id="dataset",
        baseline_dataset_version="1.0.0",
        baseline_quality_run_id="baseline-quality",
        comparison_quality_run_id="comparison-quality",
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
                alert_id="monitor-1:DRIFT_WARNING",
                code="DRIFT_WARNING",
                severity=AlertSeverity.WARNING,
                metric="distribution_drift",
                observed=0.2,
                threshold=0.1,
            ),
        ),
    )


def test_store_reopens_immutable_snapshot_and_pending_alerts(tmp_path) -> None:
    path = tmp_path / "observability.sqlite"
    store = SQLiteDatasetObservabilityRepository(path)
    snapshot = sample_snapshot()
    assert store.save(snapshot=snapshot)
    reopened = SQLiteDatasetObservabilityRepository(path)
    assert reopened.get(monitor_run_id="monitor-1") == snapshot
    assert reopened.list_snapshots(dataset_id="dataset") == (snapshot,)
    assert reopened.pending() == snapshot.alerts
    assert reopened.get(monitor_run_id="missing") is None


def test_replay_is_idempotent_but_different_content_fails_closed(tmp_path) -> None:
    store = SQLiteDatasetObservabilityRepository(tmp_path / "monitor.sqlite")
    snapshot = sample_snapshot()
    assert store.save(snapshot=snapshot)
    assert not store.save(snapshot=snapshot)
    altered = replace(
        snapshot, recorded_at=snapshot.recorded_at + timedelta(seconds=1)
    )
    with pytest.raises(ObservabilityStorageError, match="different content"):
        store.save(snapshot=altered)
    assert store.get(monitor_run_id="monitor-1") == snapshot


def test_alert_receipt_removes_pending_without_deleting_history(tmp_path) -> None:
    path = tmp_path / "monitor.sqlite"
    store = SQLiteDatasetObservabilityRepository(path)
    snapshot = sample_snapshot()
    store.save(snapshot=snapshot)
    alert_id = snapshot.alerts[0].alert_id
    assert store.mark_delivered(alert_id=alert_id)
    assert not store.mark_delivered(alert_id=alert_id)
    assert store.pending() == ()
    assert store.get(monitor_run_id="monitor-1") == snapshot
    with sqlite3.connect(path) as conn:
        events = conn.execute(
            "SELECT alert_id FROM dataset_monitor_alert_receipts"
        ).fetchall()
    assert events == [(alert_id,)]


def test_unknown_alert_acknowledgment_fails_closed(tmp_path) -> None:
    store = SQLiteDatasetObservabilityRepository(tmp_path / "monitor.sqlite")
    with pytest.raises(ObservabilityStorageError, match="does not exist"):
        store.mark_delivered(alert_id="unknown")


def test_fault_injected_alert_insert_rolls_back_snapshot(tmp_path) -> None:
    path = tmp_path / "monitor.sqlite"
    store = SQLiteDatasetObservabilityRepository(path)
    with sqlite3.connect(path) as conn:
        conn.execute(
            """
            CREATE TRIGGER reject_outbox
            BEFORE INSERT ON dataset_monitor_alert_outbox
            BEGIN SELECT RAISE(ABORT, 'injected failure'); END
            """
        )
    with pytest.raises(ObservabilityStorageError, match="transaction failed"):
        store.save(snapshot=sample_snapshot())
    assert store.get(monitor_run_id="monitor-1") is None
    assert store.pending() == ()


def test_fault_injected_ack_receipt_preserves_pending_delivery(tmp_path) -> None:
    path = tmp_path / "monitor.sqlite"
    store = SQLiteDatasetObservabilityRepository(path)
    store.save(snapshot=sample_snapshot())
    with sqlite3.connect(path) as conn:
        conn.execute(
            """
            CREATE TRIGGER reject_receipt
            BEFORE INSERT ON dataset_monitor_alert_receipts
            BEGIN SELECT RAISE(ABORT, 'injected failure'); END
            """
        )
    with pytest.raises(ObservabilityStorageError, match="acknowledgment failed"):
        store.mark_delivered(alert_id="monitor-1:DRIFT_WARNING")
    assert len(store.pending()) == 1


def test_concurrent_replay_commits_one_snapshot_and_alert(tmp_path) -> None:
    path = tmp_path / "monitor.sqlite"
    SQLiteDatasetObservabilityRepository(path)
    snapshot = sample_snapshot()

    def attempt(_i: int) -> bool:
        return SQLiteDatasetObservabilityRepository(path).save(snapshot=snapshot)

    with ThreadPoolExecutor(max_workers=6) as pool:
        results = list(pool.map(attempt, range(6)))
    assert sum(results) == 1
    store = SQLiteDatasetObservabilityRepository(path)
    assert len(store.list_snapshots(dataset_id="dataset")) == 1
    assert store.pending() == snapshot.alerts


def test_tampered_snapshot_and_alert_are_detected(tmp_path) -> None:
    path = tmp_path / "monitor.sqlite"
    store = SQLiteDatasetObservabilityRepository(path)
    store.save(snapshot=sample_snapshot())
    with sqlite3.connect(path) as conn:
        conn.execute(
            """
            UPDATE dataset_monitor_alert_outbox
            SET alert_json = '{"malicious":true}'
            """
        )
    with pytest.raises(ObservabilityStorageError, match="checksum mismatch"):
        store.pending()
    with sqlite3.connect(path) as conn:
        conn.execute(
            """
            UPDATE dataset_monitor_snapshots
            SET payload_json = '{"tampered":true}'
            """
        )
    with pytest.raises(ObservabilityStorageError, match="checksum mismatch"):
        store.get(monitor_run_id="monitor-1")


def test_bounded_query_limits_are_validated(tmp_path) -> None:
    store = SQLiteDatasetObservabilityRepository(tmp_path / "monitor.sqlite")
    for invalid in (0, -1, True, 1001):
        with pytest.raises(ObservabilityStorageError, match="limit"):
            store.list_snapshots(dataset_id="dataset", limit=invalid)
        with pytest.raises(ObservabilityStorageError, match="limit"):
            store.pending(limit=invalid)


def test_storage_never_records_raw_sample_data(tmp_path) -> None:
    path = tmp_path / "monitor.sqlite"
    store = SQLiteDatasetObservabilityRepository(path)
    store.save(snapshot=sample_snapshot())
    assert b"private candidate answer" not in path.read_bytes()
    stored = store.get(monitor_run_id="monitor-1")
    assert stored is not None
    assert not hasattr(stored, "records")


class SenderSpy:
    def __init__(self, fail: bool = False) -> None:
        self.fail = fail
        self.sent: list[str] = []

    def send(self, *, alert: MonitoringAlert) -> None:
        if self.fail:
            raise RuntimeError("provider is down")
        self.sent.append(alert.alert_id)


def test_dispatcher_retries_pending_alerts_on_sender_error(tmp_path) -> None:
    store = SQLiteDatasetObservabilityRepository(tmp_path / "monitor.sqlite")
    store.save(snapshot=sample_snapshot())
    sender = SenderSpy(fail=True)
    dispatcher = DatasetAlertDispatcher(outbox=store, sender=sender)
    with pytest.raises(AlertDeliveryError, match="retry"):
        dispatcher.dispatch_pending()
    assert len(store.pending()) == 1
    sender.fail = False
    assert dispatcher.dispatch_pending() == 1
    assert dispatcher.dispatch_pending() == 0
    assert sender.sent == ["monitor-1:DRIFT_WARNING"]


def test_invalid_storage_configuration_rejected() -> None:
    for timeout in (0, float("nan"), True):
        with pytest.raises(ObservabilityStorageError):
            SQLiteDatasetObservabilityRepository("/tmp/invalid.db", timeout=timeout)
    with pytest.raises(ObservabilityStorageError, match="file-backed"):
        SQLiteDatasetObservabilityRepository(":memory:")
