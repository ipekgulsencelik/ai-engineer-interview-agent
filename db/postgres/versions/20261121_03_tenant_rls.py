"""Enforce tenant isolation across monitoring snapshots and alert lifecycle.

Revision ID: 20261121_03
Revises: 20261110_02

Every tenant uses its own *login* role. Tenant identity is looked up using
SESSION_USER in a locked admin mapping, not a mutable application GUC.
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "20261121_03"
down_revision = "20261110_02"
branch_labels = None
depends_on = None

_TABLES = (
    "dataset_monitor_snapshots",
    "dataset_monitor_alert_outbox",
    "dataset_monitor_alert_receipts",
    "dataset_monitor_alert_delivery_events",
)


def upgrade() -> None:
    # In a production rollout, pause writers and take a verified snapshot
    # before the tenant_id backfill and the RLS policy cutover.
    op.execute("CREATE SCHEMA monitoring_security")
    op.execute(
        """
        CREATE TABLE monitoring_security.tenant_login_bindings (
            login_role NAME PRIMARY KEY,
            tenant_id TEXT NOT NULL
              CHECK (length(btrim(tenant_id)) BETWEEN 1 AND 128)
        )
        """
    )
    op.execute(
        """
        CREATE FUNCTION monitoring_security.current_tenant()
        RETURNS TEXT
        LANGUAGE sql STABLE SECURITY DEFINER
        SET search_path = pg_catalog, pg_temp
        AS $$
            SELECT binding.tenant_id
            FROM monitoring_security.tenant_login_bindings AS binding
            WHERE binding.login_role = SESSION_USER
        $$
        """
    )
    op.execute(
        "REVOKE ALL ON SCHEMA monitoring_security FROM PUBLIC"
    )
    op.execute(
        """
        REVOKE ALL ON FUNCTION monitoring_security.current_tenant()
        FROM PUBLIC
        """
    )
    op.execute(
        """
        REVOKE ALL ON monitoring_security.tenant_login_bindings
        FROM PUBLIC
        """
    )

    for table in _TABLES:
        # Existing monitoring data belongs to 'legacy'. It MUST be explicitly
        # assigned to a managed tenant before any cross-tenant rollout.
        op.add_column(
            table,
            sa.Column(
                "tenant_id",
                sa.Text(),
                nullable=False,
                server_default="legacy",
            ),
        )
        op.alter_column(
            table,
            "tenant_id",
            server_default=sa.text(
                "COALESCE(monitoring_security.current_tenant(), 'legacy')"
            ),
        )
        op.create_check_constraint(
            f"ck_{table}_tenant_not_blank",
            table,
            "length(btrim(tenant_id)) BETWEEN 1 AND 128",
        )

    # The old global PKs stay for backwards compatibility. New composite
    # references prevent cross-tenant child rows, even when the attacker
    # guesses a globally unique parent identifier.
    op.create_unique_constraint(
        "uq_monitor_snapshot_tenant",
        "dataset_monitor_snapshots",
        ["monitor_run_id", "tenant_id"],
    )
    op.create_unique_constraint(
        "uq_monitor_outbox_tenant",
        "dataset_monitor_alert_outbox",
        ["alert_id", "tenant_id"],
    )
    op.create_foreign_key(
        "fk_monitor_outbox_snapshot_tenant",
        "dataset_monitor_alert_outbox",
        "dataset_monitor_snapshots",
        ["monitor_run_id", "tenant_id"],
        ["monitor_run_id", "tenant_id"],
        ondelete="RESTRICT",
    )
    for table in (
        "dataset_monitor_alert_receipts",
        "dataset_monitor_alert_delivery_events",
    ):
        op.create_foreign_key(
            f"fk_{table}_outbox_tenant",
            table,
            "dataset_monitor_alert_outbox",
            ["alert_id", "tenant_id"],
            ["alert_id", "tenant_id"],
            ondelete="RESTRICT",
        )

    op.create_index(
        "ix_monitor_tenant_dataset_time",
        "dataset_monitor_snapshots",
        ["tenant_id", "dataset_id", "recorded_at"],
    )
    op.create_index(
        "ix_monitor_tenant_outbox",
        "dataset_monitor_alert_outbox",
        ["tenant_id", "delivered_at", "dead_lettered_at"],
    )

    # RLS must apply to ALL FOUR tables. FORCE RLS prevents the ordinary
    # table owner from silently bypassing policies. Superusers and
    # BYPASSRLS roles still bypass by PostgreSQL design and MUST NEVER
    # be used by request or worker services.
    for table in _TABLES:
        op.execute(
            f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY"
        )
        op.execute(
            f"ALTER TABLE {table} FORCE ROW LEVEL SECURITY"
        )
        op.execute(
            f"""
            CREATE POLICY tenant_isolation ON {table}
            USING (
                tenant_id = monitoring_security.current_tenant()
            )
            WITH CHECK (
                tenant_id = monitoring_security.current_tenant()
            )
            """
        )


def downgrade() -> None:
    # Data-destructive downgrade is deliberate and must not run automatically
    # in live multi-tenant deployments.
    for table in _TABLES:
        op.execute(f"DROP POLICY tenant_isolation ON {table}")
        op.execute(f"ALTER TABLE {table} DISABLE ROW LEVEL SECURITY")
        op.execute(f"ALTER TABLE {table} NO FORCE ROW LEVEL SECURITY")

    op.drop_index(
        "ix_monitor_tenant_outbox",
        table_name="dataset_monitor_alert_outbox",
    )
    op.drop_index(
        "ix_monitor_tenant_dataset_time",
        table_name="dataset_monitor_snapshots",
    )
    for table in (
        "dataset_monitor_alert_receipts",
        "dataset_monitor_alert_delivery_events",
    ):
        op.drop_constraint(
            f"fk_{table}_outbox_tenant", table, type_="foreignkey"
        )
    op.drop_constraint(
        "fk_monitor_outbox_snapshot_tenant",
        "dataset_monitor_alert_outbox",
        type_="foreignkey",
    )
    op.drop_constraint(
        "uq_monitor_outbox_tenant",
        "dataset_monitor_alert_outbox",
        type_="unique",
    )
    op.drop_constraint(
        "uq_monitor_snapshot_tenant",
        "dataset_monitor_snapshots",
        type_="unique",
    )
    for table in reversed(_TABLES):
        op.drop_constraint(
            f"ck_{table}_tenant_not_blank",
            table,
            type_="check",
        )
        op.drop_column(table, "tenant_id")
    op.execute("DROP FUNCTION monitoring_security.current_tenant()")
    op.execute("DROP TABLE monitoring_security.tenant_login_bindings")
    op.execute("DROP SCHEMA monitoring_security")
