"""Monitoring snapshots and durable outbox base schema.

Revision ID: 20261110_01
Revises:
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "20261110_01"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "dataset_monitor_snapshots",
        sa.Column("monitor_run_id", sa.Text(), primary_key=True),
        sa.Column("dataset_id", sa.Text(), nullable=False),
        sa.Column("recorded_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("payload_json", sa.Text(), nullable=False),
        sa.Column("checksum", sa.String(length=64), nullable=False),
    )
    op.create_index(
        "ix_monitor_dataset_time",
        "dataset_monitor_snapshots",
        ["dataset_id", "recorded_at"],
    )
    op.create_table(
        "dataset_monitor_alert_outbox",
        sa.Column("alert_id", sa.Text(), primary_key=True),
        sa.Column(
            "monitor_run_id", sa.Text(),
            sa.ForeignKey("dataset_monitor_snapshots.monitor_run_id"),
            nullable=False,
        ),
        sa.Column("alert_json", sa.Text(), nullable=False),
        sa.Column("checksum", sa.String(length=64), nullable=False),
        sa.Column("delivered_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index(
        "ix_monitor_pending_alerts",
        "dataset_monitor_alert_outbox",
        ["delivered_at", "alert_id"],
    )
    op.create_table(
        "dataset_monitor_alert_receipts",
        sa.Column(
            "alert_id", sa.Text(),
            sa.ForeignKey("dataset_monitor_alert_outbox.alert_id"),
            primary_key=True,
        ),
        sa.Column("delivered_at", sa.DateTime(timezone=True), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("dataset_monitor_alert_receipts")
    op.drop_index(
        "ix_monitor_pending_alerts",
        table_name="dataset_monitor_alert_outbox",
    )
    op.drop_table("dataset_monitor_alert_outbox")
    op.drop_index(
        "ix_monitor_dataset_time",
        table_name="dataset_monitor_snapshots",
    )
    op.drop_table("dataset_monitor_snapshots")
