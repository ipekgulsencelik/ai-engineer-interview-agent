"""Real PostgreSQL RLS, database RBAC and cross-tenant FK tests.

These tests require a disposable PostgreSQL 16+ service with superuser
credentials, never a shared production database.
"""

from __future__ import annotations

import os
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

import pytest

from src.evaluation.dataset.observability import (
    AlertSeverity,
    MonitoringAlert,
    MonitoringPolicy,
    MonitoringSnapshot,
    MonitoringStatus,
    ObservabilityStorageError,
)
from src.infrastructure.repositories.postgres_dataset_observability_repository import (
    PostgresDatasetObservabilityRepository,
)
from src.infrastructure.repositories.postgres_leased_dataset_alert_outbox import (
    PostgresLeasedDatasetAlertOutbox,
)


@pytest.fixture(scope="module")
def tenants():
    if not os.environ.get("POSTGRES_TEST_DSN"):
        pytest.skip("POSTGRES_TEST_DSN not set")
    psycopg = pytest.importorskip("psycopg")
    sql = psycopg.sql

    dsn = os.environ["POSTGRES_TEST_DSN"]
    prefix = f"t_{uuid4().hex[:10]}"
    password = "ephemeral-ci-only-database-password"
    definitions = {
        "a_writer": ("interview_monitor_writer", "tenant_a"),
        "b_writer": ("interview_monitor_writer", "tenant_b"),
        "a_reader": ("interview_monitor_reader", "tenant_a"),
        "b_reader": ("interview_monitor_reader", "tenant_b"),
        "a_dispatch": ("interview_monitor_dispatcher", "tenant_a"),
        "b_dispatch": ("interview_monitor_dispatcher", "tenant_b"),
        "unbound": ("interview_monitor_writer", None),
    }
    names = {key: f"{prefix}_{key}" for key in definitions}

    with psycopg.connect(dsn) as admin:
        # ClientCursor supports the operator-maintained multi-statement SQL
        # bootstrap; driver never interpolates secrets into SQL text.
        with psycopg.ClientCursor(admin) as cursor:
            cursor.execute(
                Path("db/postgres/tenant_roles.sql").read_text(
                    encoding="utf-8"
                )
            )
        admin.execute("TRUNCATE dataset_monitor_snapshots CASCADE")
        for key, (group, tenant) in definitions.items():
            login = names[key]
            admin.execute(
                sql.SQL("CREATE ROLE {} LOGIN PASSWORD {}").format(
                    sql.Identifier(login),
                    sql.Literal(password),
                )
            )
            admin.execute(
                sql.SQL("GRANT {} TO {}").format(
                    sql.Identifier(group),
                    sql.Identifier(login),
                )
            )
            if tenant is not None:
                admin.execute(
                    """
                    INSERT INTO monitoring_security.tenant_login_bindings
                    (login_role, tenant_id) VALUES (%s, %s)
                    """,
                    (login, tenant),
                )

    def connect(key: str):
        login = names[key]

        def open_connection():
            # psycopg's make_conninfo() returns keyword/value text rather
            # than the URL expected by the production factory. Authenticate
            # as the actual tenant login without weakening production checks.
            return psycopg.connect(dsn, user=login, password=password)

        return open_connection

    try:
        yield connect
    finally:
        with psycopg.connect(dsn) as admin:
            admin.execute("TRUNCATE dataset_monitor_snapshots CASCADE")
            for key, (_group, _tenant) in definitions.items():
                admin.execute(
                    """
                    DELETE FROM monitoring_security.tenant_login_bindings
                    WHERE login_role = %s
                    """,
                    (names[key],),
                )
            for login in names.values():
                admin.execute(
                    sql.SQL("DROP ROLE {}").format(sql.Identifier(login))
                )


def snapshot(index: int) -> MonitoringSnapshot:
    run_id = f"secure-run-{index}"
    return MonitoringSnapshot(
        monitor_run_id=run_id,
        dataset_id="common-dataset-name",
        dataset_version="2.0.0",
        baseline_dataset_id="common-dataset-name",
        baseline_dataset_version="1.0.0",
        baseline_quality_run_id=f"baseline-{index}",
        comparison_quality_run_id=f"comparison-{index}",
        recorded_at=datetime(2026, 11, 21, tzinfo=UTC),
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


def test_rls_is_forced_on_all_monitoring_tables(tenants) -> None:
    with tenants("a_reader")() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT relname, relrowsecurity, relforcerowsecurity
                FROM pg_catalog.pg_class
                WHERE relname LIKE 'dataset_monitor_%'
                  AND relkind = 'r'
                """
            )
            rows = cursor.fetchall()
    assert {name for name, _enabled, _forced in rows} == {
        "dataset_monitor_snapshots",
        "dataset_monitor_alert_outbox",
        "dataset_monitor_alert_receipts",
        "dataset_monitor_alert_delivery_events",
    }
    assert all(enabled and forced for _name, enabled, forced in rows)


def test_reader_has_only_own_tenant_visibility(tenants) -> None:
    a = snapshot(101)
    b = snapshot(202)
    assert PostgresDatasetObservabilityRepository(
        connect=tenants("a_writer")
    ).save(snapshot=a)
    assert PostgresDatasetObservabilityRepository(
        connect=tenants("b_writer")
    ).save(snapshot=b)

    reader_a = PostgresDatasetObservabilityRepository(
        connect=tenants("a_reader")
    )
    reader_b = PostgresDatasetObservabilityRepository(
        connect=tenants("b_reader")
    )
    assert reader_a.get(monitor_run_id=a.monitor_run_id) == a
    assert reader_a.get(monitor_run_id=b.monitor_run_id) is None
    assert reader_b.get(monitor_run_id=a.monitor_run_id) is None
    assert reader_b.get(monitor_run_id=b.monitor_run_id) == b
    assert a in reader_a.list_snapshots(dataset_id=a.dataset_id)
    assert b not in reader_a.list_snapshots(dataset_id=a.dataset_id)


def test_login_role_identity_cannot_be_replaced_with_mutable_guc(tenants) -> None:
    with tenants("b_reader")() as conn, conn.cursor() as cursor:
        cursor.execute("SELECT monitoring_security.current_tenant()")
        assert cursor.fetchone()[0] == "tenant_b"
        cursor.execute("SET app.tenant_id = 'tenant_a'")
        cursor.execute("SELECT monitoring_security.current_tenant()")
        assert cursor.fetchone()[0] == "tenant_b"
        with pytest.raises(Exception):
            # A reader has no SELECT or UPDATE privileges over the mapping.
            cursor.execute(
                "SELECT * FROM monitoring_security.tenant_login_bindings"
            )


def test_unbound_login_fails_closed_and_cannot_insert(tenants) -> None:
    with tenants("unbound")() as conn, conn.cursor() as cursor:
        cursor.execute("SELECT monitoring_security.current_tenant()")
        assert cursor.fetchone()[0] is None
    writer = PostgresDatasetObservabilityRepository(
        connect=tenants("unbound")
    )
    with pytest.raises(ObservabilityStorageError):
        writer.save(snapshot=snapshot(303))


def test_database_rbac_denies_unauthorized_writes(tenants) -> None:
    reader = PostgresDatasetObservabilityRepository(
        connect=tenants("a_reader")
    )
    with pytest.raises(ObservabilityStorageError):
        reader.save(snapshot=snapshot(304))

    dispatcher = PostgresDatasetObservabilityRepository(
        connect=tenants("a_dispatch")
    )
    with pytest.raises(ObservabilityStorageError):
        dispatcher.save(snapshot=snapshot(305))

    with tenants("a_writer")() as conn, conn.cursor() as cursor:
        with pytest.raises(Exception):
            # Writers cannot mutate lease or delivery state.
            cursor.execute(
                """
                UPDATE dataset_monitor_alert_outbox
                SET attempt_count = 2
                """
            )


def test_cross_tenant_fk_blocks_foreign_alert_attachment(tenants) -> None:
    a = snapshot(401)
    PostgresDatasetObservabilityRepository(
        connect=tenants("a_writer")
    ).save(snapshot=a)
    with tenants("b_writer")() as conn, conn.cursor() as cursor:
        with pytest.raises(Exception):
            # Even if guessed, a run ID from another tenant cannot become
            # the parent of a new tenant B alert.
            cursor.execute(
                """
                INSERT INTO dataset_monitor_alert_outbox
                  (alert_id, monitor_run_id, alert_json, checksum)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    "foreign-tenant-attachment",
                    a.monitor_run_id,
                    '{"alert_id":"foreign-tenant-attachment"}',
                    "placeholder",
                ),
            )


def test_dispatcher_only_claims_own_alerts_and_receipts(tenants) -> None:
    a = snapshot(501)
    b = snapshot(502)
    PostgresDatasetObservabilityRepository(
        connect=tenants("a_writer")
    ).save(snapshot=a)
    PostgresDatasetObservabilityRepository(
        connect=tenants("b_writer")
    ).save(snapshot=b)

    outbox_a = PostgresLeasedDatasetAlertOutbox(
        connect=tenants("a_dispatch")
    )
    outbox_b = PostgresLeasedDatasetAlertOutbox(
        connect=tenants("b_dispatch")
    )
    a_leases = outbox_a.claim(
        worker_id="tenant-a-worker", limit=100, lease_seconds=60
    )
    b_leases = outbox_b.claim(
        worker_id="tenant-b-worker", limit=100, lease_seconds=60
    )
    assert {v.alert.alert_id for v in a_leases} == {
        alert.alert_id
        for saved in PostgresDatasetObservabilityRepository(
            connect=tenants("a_reader")
        ).list_snapshots(dataset_id=a.dataset_id)
        for alert in saved.alerts
    }
    assert len(b_leases) >= 1
    assert set(x.alert.alert_id for x in a_leases).isdisjoint(
        {x.alert.alert_id for x in b_leases}
    )
    for lease in a_leases:
        assert outbox_a.acknowledge(lease=lease)
    for lease in b_leases:
        assert outbox_b.acknowledge(lease=lease)
    assert outbox_a.delivery_events(
        alert_id=b.alerts[0].alert_id
    ) == ()
    assert outbox_b.delivery_events(
        alert_id=a.alerts[0].alert_id
    ) == ()


def test_cross_tenant_direct_update_is_zero_rows(tenants) -> None:
    a = snapshot(601)
    PostgresDatasetObservabilityRepository(
        connect=tenants("a_writer")
    ).save(snapshot=a)
    with tenants("b_dispatch")() as conn, conn.cursor() as cursor:
        cursor.execute(
            """
            UPDATE dataset_monitor_alert_outbox
            SET last_reason_code = %s
            WHERE alert_id = %s
            """,
            ("SPOOFED", a.alerts[0].alert_id),
        )
        assert cursor.rowcount == 0
