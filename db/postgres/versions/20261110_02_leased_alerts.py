"""Fenced outbox delivery, durable retries, and DLQ.

Revision ID: 20261110_02
Revises: 20261110_01
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "20261110_02"
down_revision = "20261110_01"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "dataset_monitor_alert_outbox",
        sa.Column("lease_token", sa.Text(), nullable=True),
    )
    op.add_column(
        "dataset_monitor_alert_outbox",
        sa.Column("lease_owner", sa.Text(), nullable=True),
    )
    op.add_column(
        "dataset_monitor_alert_outbox",
        sa.Column("lease_expires_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "dataset_monitor_alert_outbox",
        sa.Column(
            "attempt_count", sa.Integer(), nullable=False,
            server_default="0",
        ),
    )
    op.add_column(
        "dataset_monitor_alert_outbox",
        sa.Column("next_attempt_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "dataset_monitor_alert_outbox",
        sa.Column("dead_lettered_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "dataset_monitor_alert_outbox",
        sa.Column("last_reason_code", sa.Text(), nullable=True),
    )
    op.create_check_constraint(
        "ck_monitor_alert_attempt_count_nonnegative",
        "dataset_monitor_alert_outbox",
        "attempt_count >= 0",
    )
    op.create_index(
        "ix_monitor_alert_lease_ready",
        "dataset_monitor_alert_outbox",
        [
            "delivered_at", "dead_lettered_at",
            "next_attempt_at", "lease_expires_at",
        ],
    )
    op.create_table(
        "dataset_monitor_alert_delivery_events",
        sa.Column(
            "event_seq", sa.BigInteger(),
            sa.Identity(always=True), nullable=False, unique=True,
        ),
        sa.Column("event_id", sa.Text(), primary_key=True),
        sa.Column(
            "alert_id", sa.Text(),
            sa.ForeignKey("dataset_monitor_alert_outbox.alert_id"),
            nullable=False,
        ),
        sa.Column("event_type", sa.Text(), nullable=False),
        sa.Column("attempt_count", sa.Integer(), nullable=False),
        sa.Column("reason_code", sa.Text(), nullable=True),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(
        "ix_monitor_alert_events_alert",
        "dataset_monitor_alert_delivery_events",
        ["alert_id", "occurred_at"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_monitor_alert_events_alert",
        table_name="dataset_monitor_alert_delivery_events",
    )
    op.drop_table("dataset_monitor_alert_delivery_events")
    op.drop_index(
        "ix_monitor_alert_lease_ready",
        table_name="dataset_monitor_alert_outbox",
    )
    op.drop_constraint(
        "ck_monitor_alert_attempt_count_nonnegative",
        "dataset_monitor_alert_outbox",
        type_="check",
    )
    for column in (
        "last_reason_code",
        "dead_lettered_at",
        "next_attempt_at",
        "attempt_count",
        "lease_expires_at",
        "lease_owner",
        "lease_token",
    ):
        op.drop_column("dataset_monitor_alert_outbox", column)
