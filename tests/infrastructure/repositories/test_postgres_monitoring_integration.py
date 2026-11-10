"""Real PostgreSQL integration contracts; skipped outside configured PG CI."""

from __future__ import annotations

import os
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from datetime import UTC, datetime, timedelta

import pytest

from src.evaluation.dataset.observability import (
    AlertLeaseError,
    AlertRetryPolicy,
    AlertSeverity,
    MonitoringAlert,
    MonitoringPolicy,
    MonitoringSnapshot,
    MonitoringStatus,
    ObservabilityStorageError,
)
from src.infrastructure.repositories.postgres_connection import (
    PsycopgConnectionFactory,
)
from src.infrastructure.repositories.postgres_dataset_observability_repository import (
    PostgresDatasetObservabilityRepository,
)
from src.infrastructure.repositories.postgres_leased_dataset_alert_outbox import (
    PostgresLeasedDatasetAlertOutbox,
)

_DSN = os.environ.get("POSTGRES_TEST_DSN")


@pytest.fixture
def pg_connection():
    if not _DSN:
        pytest.skip("POSTGRES_TEST_DSN not set")
    pytest.importorskip("psycopg")
    factory = PsycopgConnectionFactory(
        dsn=_DSN,
        require_tls=False,  # localhost CI only; production defaults to TLS
    )
    # Tests run after "alembic upgrade head", and are isolated per test.
    with factory() as conn, conn.cursor() as cursor:
        cursor.execute(
            "TRUNCATE dataset_monitor_snapshots CASCADE"
        )
    return factory


class FixedClock:
    def __init__(self) -> None:
        self.value = datetime(2026, 11, 10, 12, tzinfo=UTC)

    def now(self) -> datetime:
        return self.value

    def advance(self, seconds: int) -> None:
        self.value += timedelta(seconds=seconds)


def snapshot(index: int = 0) -> MonitoringSnapshot:
    alert = MonitoringAlert(
        alert_id=f"pg-run-{index}:DRIFT_WARNING",
        code="DRIFT_WARNING",
        severity=AlertSeverity.WARNING,
        metric="distribution_drift",
        observed=0.2,
        threshold=0.1,
    )
    return MonitoringSnapshot(
        monitor_run_id=f"pg-run-{index}",
        dataset_id="integration",
        dataset_version="2.0.0",
        baseline_dataset_id="integration",
        baseline_dataset_version="1.0.0",
        baseline_quality_run_id=f"baseline-{index}",
        comparison_quality_run_id=f"comparison-{index}",
        recorded_at=datetime(2026, 11, 10, 12, tzinfo=UTC),
        record_count=10,
        baseline_pass_rate=1.0,
        comparison_pass_rate=0.9,
        pass_rate_drop=0.1,
        drift_score=0.2,
        status=MonitoringStatus.WARNING,
        policy=MonitoringPolicy(),
        alerts=(alert,),
    )


def test_alembic_created_schema_at_expected_head(pg_connection) -> None:
    with pg_connection() as conn, conn.cursor() as cursor:
        cursor.execute("SELECT version_num FROM alembic_version")
        assert cursor.fetchone()[0] == "20261110_02"
        cursor.execute(
            """
            SELECT column_name FROM information_schema.columns
            WHERE table_name = 'dataset_monitor_alert_outbox'
            """
        )
        columns = {row[0] for row in cursor.fetchall()}
    assert {"lease_token", "attempt_count", "dead_lettered_at"} <= columns


def test_snapshot_and_alert_outbox_roundtrip_across_connections(
    pg_connection,
) -> None:
    writer = PostgresDatasetObservabilityRepository(connect=pg_connection)
    value = snapshot()
    assert writer.save(snapshot=value)
    assert not writer.save(snapshot=value)
    reader = PostgresDatasetObservabilityRepository(connect=pg_connection)
    assert reader.get(monitor_run_id=value.monitor_run_id) == value
    assert reader.list_snapshots(dataset_id="integration") == (value,)


def test_immutable_monitor_run_conflict_is_rejected(pg_connection) -> None:
    writer = PostgresDatasetObservabilityRepository(connect=pg_connection)
    original = snapshot()
    writer.save(snapshot=original)
    changed = replace(original, recorded_at=original.recorded_at + timedelta(seconds=1))
    with pytest.raises(ObservabilityStorageError, match="different content"):
        writer.save(snapshot=changed)
    assert writer.get(monitor_run_id=original.monitor_run_id) == original


def test_multi_worker_skip_locked_claims_each_alert_once(pg_connection) -> None:
    writer = PostgresDatasetObservabilityRepository(connect=pg_connection)
    for index in range(10):
        writer.save(snapshot=snapshot(index))
    clock = FixedClock()
    outbox = PostgresLeasedDatasetAlertOutbox(connect=pg_connection, clock=clock)

    def attempt(index: int):
        return outbox.claim(
            worker_id=f"worker-{index}", limit=3, lease_seconds=60
        )

    with ThreadPoolExecutor(max_workers=5) as pool:
        groups = list(pool.map(attempt, range(5)))
    leases = [lease for group in groups for lease in group]
    assert len(leases) == 10
    assert len({lease.alert.alert_id for lease in leases}) == 10
    for lease in leases:
        assert outbox.acknowledge(lease=lease)
    assert outbox.claim(worker_id="last", limit=20, lease_seconds=60) == ()


def test_expired_lease_backoff_fencing_and_audited_delivery(
    pg_connection,
) -> None:
    value = snapshot()
    writer = PostgresDatasetObservabilityRepository(connect=pg_connection)
    writer.save(snapshot=value)
    clock = FixedClock()
    outbox = PostgresLeasedDatasetAlertOutbox(
        connect=pg_connection,
        clock=clock,
        policy=AlertRetryPolicy(
            max_attempts=3, initial_delay_seconds=10, max_delay_seconds=20
        ),
    )
    lease = outbox.claim(worker_id="a", limit=1, lease_seconds=5)[0]
    clock.advance(5)
    assert outbox.claim(worker_id="b", limit=1, lease_seconds=5) == ()
    with pytest.raises(AlertLeaseError):
        outbox.acknowledge(lease=lease)
    clock.advance(10)
    second = outbox.claim(worker_id="b", limit=1, lease_seconds=30)[0]
    assert second.token != lease.token
    assert second.attempt == 2
    with pytest.raises(AlertLeaseError):
        outbox.fail(lease=lease, reason_code="SENDER_FAILURE")
    assert outbox.acknowledge(lease=second)
    assert outbox.delivery_events(alert_id=lease.alert.alert_id)[-1][0] == (
        "delivered"
    )


def test_terminal_dead_letter_and_manual_requeue(pg_connection) -> None:
    writer = PostgresDatasetObservabilityRepository(connect=pg_connection)
    writer.save(snapshot=snapshot())
    clock = FixedClock()
    outbox = PostgresLeasedDatasetAlertOutbox(
        connect=pg_connection,
        clock=clock,
        policy=AlertRetryPolicy(max_attempts=1),
    )
    lease = outbox.claim(worker_id="a", limit=1, lease_seconds=30)[0]
    assert outbox.fail(
        lease=lease, reason_code="SENDER_FAILURE"
    ).dead_lettered
    assert outbox.dead_letters() == snapshot().alerts
    assert outbox.requeue(alert_id=lease.alert.alert_id)
    assert not outbox.requeue(alert_id=lease.alert.alert_id)
    assert outbox.dead_letters() == ()
    next_lease = outbox.claim(worker_id="a", limit=1, lease_seconds=30)[0]
    assert next_lease.attempt == 1
    assert outbox.acknowledge(lease=next_lease)


def test_failed_receipt_rolls_back_delivery_transition(pg_connection) -> None:
    writer = PostgresDatasetObservabilityRepository(connect=pg_connection)
    writer.save(snapshot=snapshot())
    clock = FixedClock()
    outbox = PostgresLeasedDatasetAlertOutbox(
        connect=pg_connection,
        clock=clock,
    )
    lease = outbox.claim(worker_id="a", limit=1, lease_seconds=30)[0]

    with pg_connection() as conn, conn.cursor() as cursor:
        cursor.execute(
            """
            ALTER TABLE dataset_monitor_alert_receipts
            ADD CONSTRAINT reject_receipts
            CHECK (FALSE)
            """
        )
    try:
        with pytest.raises(ObservabilityStorageError, match="receipt"):
            outbox.acknowledge(lease=lease)
        assert outbox.delivery_events(
            alert_id=lease.alert.alert_id
        ) == (("claimed", 1, None),)
    finally:
        with pg_connection() as conn, conn.cursor() as cursor:
            cursor.execute(
                """
                ALTER TABLE dataset_monitor_alert_receipts
                DROP CONSTRAINT reject_receipts
                """
            )
    assert outbox.acknowledge(lease=lease)


def test_monitoring_content_is_not_written_to_delivery_audit(pg_connection) -> None:
    writer = PostgresDatasetObservabilityRepository(connect=pg_connection)
    writer.save(snapshot=snapshot())
    outbox = PostgresLeasedDatasetAlertOutbox(connect=pg_connection)
    lease = outbox.claim(worker_id="worker", limit=1, lease_seconds=30)[0]
    outbox.fail(lease=lease, reason_code="SENDER_FAILURE")
    events = outbox.delivery_events(alert_id=lease.alert.alert_id)
    assert events[-1] == ("retry", 1, "SENDER_FAILURE")
