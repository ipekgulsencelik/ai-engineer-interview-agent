"""SQLite adapter for fenced leases, bounded retry, and dead-letter handling.

All state transitions take BEGIN IMMEDIATE locks. Expired lease tokens may
never acknowledge, and an external send is never inside the SQL transaction.
"""

from __future__ import annotations

import re
import sqlite3
from contextlib import closing
from datetime import UTC, datetime, timedelta
from pathlib import Path
from uuid import uuid4

from src.evaluation.dataset.observability.delivery import (
    AlertFailureOutcome,
    AlertLease,
    AlertLeaseError,
    AlertRetryPolicy,
    DeliveryClock,
    UTCDeliveryClock,
)
from src.evaluation.dataset.observability.errors import ObservabilityStorageError
from src.evaluation.dataset.observability.models import MonitoringAlert
from src.evaluation.dataset.observability.serialization import (
)
from src.infrastructure.repositories.sqlite_dataset_observability_repository import (
    SQLiteDatasetObservabilityRepository,
    _decode_alert,
)

_REASON = re.compile(r"[A-Z][A-Z0-9_]{0,63}")


class SQLiteLeasedDatasetAlertOutbox:
    """Upgrade existing monitoring outbox in place, preserving original rows."""

    def __init__(
        self,
        path: str | Path,
        *,
        policy: AlertRetryPolicy | None = None,
        clock: DeliveryClock | None = None,
        timeout: float = 10.0,
    ) -> None:
        self._path = str(path)
        self._policy = policy if policy is not None else AlertRetryPolicy()
        self._clock = clock if clock is not None else UTCDeliveryClock()
        # Ensures the existing outbox and snapshot tables are created first.
        SQLiteDatasetObservabilityRepository(self._path, timeout=timeout)
        self._timeout = timeout
        self._migrate()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._path, timeout=self._timeout)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def _now(self) -> datetime:
        now = self._clock.now()
        if (
            not isinstance(now, datetime)
            or now.tzinfo is None
            or now.utcoffset() is None
        ):
            raise ValueError("delivery clock must be timezone-aware")
        return now.astimezone(UTC)

    def _migrate(self) -> None:
        columns = {
            "lease_token": "TEXT",
            "lease_owner": "TEXT",
            "lease_expires_at": "TEXT",
            "attempt_count": "INTEGER NOT NULL DEFAULT 0",
            "next_attempt_at": "TEXT",
            "dead_lettered_at": "TEXT",
            "last_reason_code": "TEXT",
        }
        try:
            with closing(self._connect()) as conn, conn:
                conn.execute("BEGIN IMMEDIATE")
                previous = {
                    row[1]
                    for row in conn.execute(
                        "PRAGMA table_info(dataset_monitor_alert_outbox)"
                    )
                }
                for column, definition in columns.items():
                    if column not in previous:
                        conn.execute(
                            "ALTER TABLE dataset_monitor_alert_outbox "
                            f"ADD COLUMN {column} {definition}"
                        )
                conn.execute(
                    """
                    CREATE INDEX IF NOT EXISTS ix_monitor_alert_lease_ready
                    ON dataset_monitor_alert_outbox
                    (delivered_at, dead_lettered_at, next_attempt_at,
                     lease_expires_at)
                    """
                )
                conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS dataset_monitor_alert_delivery_events (
                        event_id TEXT PRIMARY KEY,
                        alert_id TEXT NOT NULL,
                        event_type TEXT NOT NULL,
                        attempt_count INTEGER NOT NULL,
                        reason_code TEXT,
                        occurred_at TEXT NOT NULL,
                        FOREIGN KEY (alert_id)
                          REFERENCES dataset_monitor_alert_outbox(alert_id)
                    )
                    """
                )
                conn.execute(
                    """
                    CREATE INDEX IF NOT EXISTS ix_monitor_alert_events_alert
                    ON dataset_monitor_alert_delivery_events(alert_id, occurred_at)
                    """
                )
        except sqlite3.DatabaseError as exc:
            raise ObservabilityStorageError(
                "leased outbox schema migration failed"
            ) from exc

    @staticmethod
    def _event(
        conn: sqlite3.Connection,
        *,
        alert_id: str,
        event_type: str,
        attempts: int,
        now: datetime,
        reason_code: str | None = None,
    ) -> None:
        conn.execute(
            """
            INSERT INTO dataset_monitor_alert_delivery_events
            (event_id, alert_id, event_type, attempt_count,
             reason_code, occurred_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (uuid4().hex, alert_id, event_type, attempts,
             reason_code, now.isoformat()),
        )

    def _recover_expired(
        self, conn: sqlite3.Connection, now: datetime
    ) -> None:
        rows = conn.execute(
            """
            SELECT alert_id, attempt_count
            FROM dataset_monitor_alert_outbox
            WHERE delivered_at IS NULL AND dead_lettered_at IS NULL
              AND lease_token IS NOT NULL AND lease_expires_at <= ?
            """,
            (now.isoformat(),),
        ).fetchall()
        for alert_id, attempts in rows:
            exhausted = attempts >= self._policy.max_attempts
            next_attempt = (
                None if exhausted
                else (now + timedelta(
                    seconds=self._policy.delay_for_attempt(attempts)
                )).isoformat()
            )
            conn.execute(
                """
                UPDATE dataset_monitor_alert_outbox
                SET lease_token = NULL, lease_owner = NULL,
                    lease_expires_at = NULL, next_attempt_at = ?,
                    dead_lettered_at = ?, last_reason_code = ?
                WHERE alert_id = ?
                """,
                (
                    next_attempt,
                    now.isoformat() if exhausted else None,
                    "LEASE_EXPIRED",
                    alert_id,
                ),
            )
            self._event(
                conn,
                alert_id=alert_id,
                event_type="dead_letter" if exhausted else "lease_expired",
                attempts=attempts,
                now=now,
                reason_code="LEASE_EXPIRED",
            )

    def claim(
        self, *, worker_id: str, limit: int, lease_seconds: int
    ) -> tuple[AlertLease, ...]:
        if not isinstance(worker_id, str) or not worker_id.strip():
            raise ValueError("worker_id must be non-empty")
        if type(limit) is not int or not 1 <= limit <= 1000:
            raise ValueError("limit must be in [1, 1000]")
        if type(lease_seconds) is not int or not 1 <= lease_seconds <= 86400:
            raise ValueError("lease_seconds must be in [1, 86400]")
        now = self._now()
        expires_at = now + timedelta(seconds=lease_seconds)
        try:
            with closing(self._connect()) as conn, conn:
                conn.execute("BEGIN IMMEDIATE")
                self._recover_expired(conn, now)
                rows = conn.execute(
                    """
                    SELECT a.alert_id, a.alert_json, a.checksum, a.attempt_count
                    FROM dataset_monitor_alert_outbox AS a
                    JOIN dataset_monitor_snapshots AS s
                      ON a.monitor_run_id = s.monitor_run_id
                    WHERE a.delivered_at IS NULL AND a.dead_lettered_at IS NULL
                      AND a.lease_token IS NULL
                      AND (a.next_attempt_at IS NULL OR a.next_attempt_at <= ?)
                      AND a.attempt_count < ?
                    ORDER BY s.recorded_at, a.alert_id LIMIT ?
                    """,
                    (now.isoformat(), self._policy.max_attempts, limit),
                ).fetchall()
                leases: list[AlertLease] = []
                for alert_id, payload, checksum, prior_attempts in rows:
                    alert = _decode_alert(payload, checksum)
                    token = uuid4().hex
                    attempt = prior_attempts + 1
                    conn.execute(
                        """
                        UPDATE dataset_monitor_alert_outbox
                        SET lease_token = ?, lease_owner = ?,
                            lease_expires_at = ?, attempt_count = ?,
                            next_attempt_at = NULL
                        WHERE alert_id = ?
                        """,
                        (token, worker_id, expires_at.isoformat(), attempt, alert_id),
                    )
                    self._event(
                        conn, alert_id=alert_id, event_type="claimed",
                        attempts=attempt, now=now,
                    )
                    leases.append(
                        AlertLease(
                            alert=alert,
                            token=token,
                            worker_id=worker_id,
                            attempt=attempt,
                            expires_at=expires_at,
                        )
                    )
                return tuple(leases)
        except sqlite3.DatabaseError as exc:
            raise ObservabilityStorageError("alert lease claim failed") from exc

    def _owned(
        self,
        conn: sqlite3.Connection,
        *,
        lease: AlertLease,
        now: datetime,
    ) -> tuple[int, str, str]:
        row = conn.execute(
            """
            SELECT attempt_count, alert_json, checksum
            FROM dataset_monitor_alert_outbox
            WHERE alert_id = ? AND lease_token = ? AND lease_owner = ?
              AND attempt_count = ? AND lease_expires_at > ?
              AND delivered_at IS NULL AND dead_lettered_at IS NULL
            """,
            (
                lease.alert.alert_id, lease.token, lease.worker_id,
                lease.attempt, now.isoformat(),
            ),
        ).fetchone()
        if row is None:
            raise AlertLeaseError("alert lease expired or ownership was lost")
        alert = _decode_alert(row[1], row[2])
        if alert != lease.alert:
            raise AlertLeaseError("claimed alert content changed")
        return row

    def acknowledge(self, *, lease: AlertLease) -> bool:
        now = self._now()
        try:
            with closing(self._connect()) as conn, conn:
                conn.execute("BEGIN IMMEDIATE")
                self._owned(conn, lease=lease, now=now)
                conn.execute(
                    """
                    UPDATE dataset_monitor_alert_outbox
                    SET delivered_at = ?, lease_token = NULL,
                        lease_owner = NULL, lease_expires_at = NULL
                    WHERE alert_id = ?
                    """,
                    (now.isoformat(), lease.alert.alert_id),
                )
                conn.execute(
                    """
                    INSERT INTO dataset_monitor_alert_receipts
                    (alert_id, delivered_at) VALUES (?, ?)
                    """,
                    (lease.alert.alert_id, now.isoformat()),
                )
                self._event(
                    conn, alert_id=lease.alert.alert_id,
                    event_type="delivered", attempts=lease.attempt, now=now,
                )
                return True
        except sqlite3.DatabaseError as exc:
            raise ObservabilityStorageError(
                "alert delivery receipt transaction failed"
            ) from exc

    def fail(
        self, *, lease: AlertLease, reason_code: str
    ) -> AlertFailureOutcome:
        if not isinstance(reason_code, str) or _REASON.fullmatch(reason_code) is None:
            raise ValueError("reason_code must be a stable uppercase machine code")
        now = self._now()
        terminal = lease.attempt >= self._policy.max_attempts
        next_at = (
            None if terminal
            else (now + timedelta(
                seconds=self._policy.delay_for_attempt(lease.attempt)
            )).isoformat()
        )
        try:
            with closing(self._connect()) as conn, conn:
                conn.execute("BEGIN IMMEDIATE")
                self._owned(conn, lease=lease, now=now)
                conn.execute(
                    """
                    UPDATE dataset_monitor_alert_outbox
                    SET lease_token = NULL, lease_owner = NULL,
                        lease_expires_at = NULL, next_attempt_at = ?,
                        dead_lettered_at = ?, last_reason_code = ?
                    WHERE alert_id = ?
                    """,
                    (
                        next_at, now.isoformat() if terminal else None,
                        reason_code, lease.alert.alert_id,
                    ),
                )
                self._event(
                    conn,
                    alert_id=lease.alert.alert_id,
                    event_type="dead_letter" if terminal else "retry",
                    attempts=lease.attempt,
                    reason_code=reason_code,
                    now=now,
                )
        except sqlite3.DatabaseError as exc:
            raise ObservabilityStorageError(
                "alert failure transition failed"
            ) from exc
        return AlertFailureOutcome(
            alert_id=lease.alert.alert_id,
            attempt=lease.attempt,
            dead_lettered=terminal,
        )

    def dead_letters(
        self, *, limit: int = 100
    ) -> tuple[MonitoringAlert, ...]:
        if type(limit) is not int or not 1 <= limit <= 1000:
            raise ValueError("limit must be in [1, 1000]")
        try:
            with closing(self._connect()) as conn:
                rows = conn.execute(
                    """
                    SELECT alert_json, checksum
                    FROM dataset_monitor_alert_outbox
                    WHERE dead_lettered_at IS NOT NULL
                    ORDER BY dead_lettered_at, alert_id LIMIT ?
                    """,
                    (limit,),
                ).fetchall()
        except sqlite3.DatabaseError as exc:
            raise ObservabilityStorageError("dead-letter query failed") from exc
        return tuple(_decode_alert(*row) for row in rows)

    def requeue(self, *, alert_id: str) -> bool:
        """Explicit operator action: reset attempts and preserve history."""
        now = self._now()
        try:
            with closing(self._connect()) as conn, conn:
                conn.execute("BEGIN IMMEDIATE")
                row = conn.execute(
                    """
                    SELECT dead_lettered_at, alert_json, checksum
                    FROM dataset_monitor_alert_outbox
                    WHERE alert_id = ? AND delivered_at IS NULL
                    """,
                    (alert_id,),
                ).fetchone()
                if row is None:
                    raise AlertLeaseError("alert is missing or already delivered")
                _decode_alert(row[1], row[2])
                if row[0] is None:
                    return False
                conn.execute(
                    """
                    UPDATE dataset_monitor_alert_outbox
                    SET dead_lettered_at = NULL, attempt_count = 0,
                        next_attempt_at = NULL, last_reason_code = NULL
                    WHERE alert_id = ?
                    """,
                    (alert_id,),
                )
                self._event(
                    conn, alert_id=alert_id, event_type="requeued",
                    attempts=0, now=now,
                )
                return True
        except sqlite3.DatabaseError as exc:
            raise ObservabilityStorageError("alert requeue failed") from exc

    def delivery_events(
        self, *, alert_id: str
    ) -> tuple[tuple[str, int, str | None], ...]:
        """Read an append-only, metadata-only history in event order."""
        try:
            with closing(self._connect()) as conn:
                rows = conn.execute(
                    """
                    SELECT event_type, attempt_count, reason_code
                    FROM dataset_monitor_alert_delivery_events
                    WHERE alert_id = ?
                    ORDER BY rowid
                    """,
                    (alert_id,),
                ).fetchall()
        except sqlite3.DatabaseError as exc:
            raise ObservabilityStorageError(
                "delivery audit lookup failed"
            ) from exc
        return tuple(rows)
