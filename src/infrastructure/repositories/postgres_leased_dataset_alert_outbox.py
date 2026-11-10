"""PostgreSQL leased alert outbox, with SKIP LOCKED worker coordination."""

from __future__ import annotations

import re
from datetime import UTC, datetime, timedelta
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
from src.infrastructure.repositories.postgres_connection import (
    PostgresConnectionPort,
)
from src.infrastructure.repositories.postgres_dataset_observability_repository import (
    _decode_alert,
)

_REASON = re.compile(r"[A-Z][A-Z0-9_]{0,63}")


class PostgresLeasedDatasetAlertOutbox:
    """Concurrent, token-fenced delivery adapter; Alembic owns migrations."""

    def __init__(
        self,
        *,
        connect: PostgresConnectionPort,
        policy: AlertRetryPolicy | None = None,
        clock: DeliveryClock | None = None,
    ) -> None:
        self._connect = connect
        self._policy = policy if policy is not None else AlertRetryPolicy()
        self._clock = clock if clock is not None else UTCDeliveryClock()

    def _now(self) -> datetime:
        current = self._clock.now()
        if (
            not isinstance(current, datetime)
            or current.tzinfo is None
            or current.utcoffset() is None
        ):
            raise ValueError("delivery clock must be timezone-aware")
        return current.astimezone(UTC)

    @staticmethod
    def _event(
        cursor: object,
        *,
        alert_id: str,
        event_type: str,
        attempts: int,
        now: datetime,
        reason_code: str | None = None,
    ) -> None:
        cursor.execute(  # type: ignore[attr-defined]
            """
            INSERT INTO dataset_monitor_alert_delivery_events (
                event_id, alert_id, event_type, attempt_count,
                reason_code, occurred_at
            ) VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (uuid4().hex, alert_id, event_type, attempts, reason_code, now),
        )

    def _recover_expired(self, cursor: object, now: datetime) -> None:
        """Recover a bounded batch, without blocking workers holding rows."""
        cursor.execute(  # type: ignore[attr-defined]
            """
            SELECT alert_id, attempt_count
            FROM dataset_monitor_alert_outbox
            WHERE delivered_at IS NULL AND dead_lettered_at IS NULL
              AND lease_token IS NOT NULL AND lease_expires_at <= %s
            ORDER BY lease_expires_at, alert_id
            LIMIT 1000 FOR UPDATE SKIP LOCKED
            """,
            (now,),
        )
        rows = cursor.fetchall()  # type: ignore[attr-defined]
        for alert_id, attempts in rows:
            terminal = attempts >= self._policy.max_attempts
            next_at = (
                None if terminal else now + timedelta(
                    seconds=self._policy.delay_for_attempt(attempts)
                )
            )
            cursor.execute(  # type: ignore[attr-defined]
                """
                UPDATE dataset_monitor_alert_outbox
                SET lease_token = NULL, lease_owner = NULL,
                    lease_expires_at = NULL, next_attempt_at = %s,
                    dead_lettered_at = %s, last_reason_code = 'LEASE_EXPIRED'
                WHERE alert_id = %s
                """,
                (next_at, now if terminal else None, alert_id),
            )
            self._event(
                cursor,
                alert_id=alert_id,
                event_type="dead_letter" if terminal else "lease_expired",
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
        expires = now + timedelta(seconds=lease_seconds)
        try:
            with self._connect() as conn, conn.cursor() as cursor:
                self._recover_expired(cursor, now)
                cursor.execute(
                    """
                    SELECT a.alert_id, a.alert_json, a.checksum,
                           a.attempt_count
                    FROM dataset_monitor_alert_outbox AS a
                    JOIN dataset_monitor_snapshots AS s
                      ON s.monitor_run_id = a.monitor_run_id
                    WHERE a.delivered_at IS NULL
                      AND a.dead_lettered_at IS NULL
                      AND a.lease_token IS NULL
                      AND (a.next_attempt_at IS NULL OR a.next_attempt_at <= %s)
                      AND a.attempt_count < %s
                    ORDER BY s.recorded_at, a.alert_id
                    LIMIT %s FOR UPDATE OF a SKIP LOCKED
                    """,
                    (now, self._policy.max_attempts, limit),
                )
                selected = cursor.fetchall()
                leases: list[AlertLease] = []
                for alert_id, payload, checksum, attempts in selected:
                    alert = _decode_alert(payload, checksum)
                    token = uuid4().hex
                    attempt = attempts + 1
                    cursor.execute(
                        """
                        UPDATE dataset_monitor_alert_outbox
                        SET lease_token = %s, lease_owner = %s,
                            lease_expires_at = %s, attempt_count = %s,
                            next_attempt_at = NULL
                        WHERE alert_id = %s
                        """,
                        (token, worker_id, expires, attempt, alert_id),
                    )
                    self._event(
                        cursor,
                        alert_id=alert_id,
                        event_type="claimed",
                        attempts=attempt,
                        now=now,
                    )
                    leases.append(
                        AlertLease(
                            alert=alert,
                            token=token,
                            worker_id=worker_id,
                            attempt=attempt,
                            expires_at=expires,
                        )
                    )
                return tuple(leases)
        except ObservabilityStorageError:
            raise
        except Exception as exc:
            raise ObservabilityStorageError(
                "PostgreSQL alert claim failed"
            ) from exc

    def _owned(self, cursor: object, *, lease: AlertLease, now: datetime) -> None:
        cursor.execute(  # type: ignore[attr-defined]
            """
            SELECT alert_json, checksum
            FROM dataset_monitor_alert_outbox
            WHERE alert_id = %s AND lease_token = %s
              AND lease_owner = %s AND attempt_count = %s
              AND lease_expires_at > %s
              AND delivered_at IS NULL AND dead_lettered_at IS NULL
            FOR UPDATE
            """,
            (
                lease.alert.alert_id, lease.token, lease.worker_id,
                lease.attempt, now,
            ),
        )
        row = cursor.fetchone()  # type: ignore[attr-defined]
        if row is None:
            raise AlertLeaseError("lease expired or ownership lost")
        if _decode_alert(row[0], row[1]) != lease.alert:
            raise AlertLeaseError("claimed alert has changed")

    def acknowledge(self, *, lease: AlertLease) -> bool:
        now = self._now()
        try:
            with self._connect() as conn, conn.cursor() as cursor:
                self._owned(cursor, lease=lease, now=now)
                cursor.execute(
                    """
                    UPDATE dataset_monitor_alert_outbox
                    SET delivered_at = %s, lease_token = NULL,
                        lease_owner = NULL, lease_expires_at = NULL
                    WHERE alert_id = %s
                    """,
                    (now, lease.alert.alert_id),
                )
                cursor.execute(
                    """
                    INSERT INTO dataset_monitor_alert_receipts
                        (alert_id, delivered_at) VALUES (%s, %s)
                    """,
                    (lease.alert.alert_id, now),
                )
                self._event(
                    cursor, alert_id=lease.alert.alert_id,
                    event_type="delivered", attempts=lease.attempt, now=now,
                )
                return True
        except (AlertLeaseError, ObservabilityStorageError):
            raise
        except Exception as exc:
            raise ObservabilityStorageError(
                "PostgreSQL delivery receipt failed"
            ) from exc

    def fail(
        self, *, lease: AlertLease, reason_code: str
    ) -> AlertFailureOutcome:
        if not isinstance(reason_code, str) or not _REASON.fullmatch(reason_code):
            raise ValueError("reason_code must be a stable uppercase code")
        now = self._now()
        terminal = lease.attempt >= self._policy.max_attempts
        retry_at = (
            None if terminal else now + timedelta(
                seconds=self._policy.delay_for_attempt(lease.attempt)
            )
        )
        try:
            with self._connect() as conn, conn.cursor() as cursor:
                self._owned(cursor, lease=lease, now=now)
                cursor.execute(
                    """
                    UPDATE dataset_monitor_alert_outbox
                    SET lease_token = NULL, lease_owner = NULL,
                        lease_expires_at = NULL, next_attempt_at = %s,
                        dead_lettered_at = %s, last_reason_code = %s
                    WHERE alert_id = %s
                    """,
                    (
                        retry_at, now if terminal else None, reason_code,
                        lease.alert.alert_id,
                    ),
                )
                self._event(
                    cursor, alert_id=lease.alert.alert_id,
                    event_type="dead_letter" if terminal else "retry",
                    attempts=lease.attempt,
                    now=now,
                    reason_code=reason_code,
                )
        except (AlertLeaseError, ObservabilityStorageError):
            raise
        except Exception as exc:
            raise ObservabilityStorageError(
                "PostgreSQL alert retry transition failed"
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
            with self._connect() as conn, conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT alert_json, checksum
                    FROM dataset_monitor_alert_outbox
                    WHERE dead_lettered_at IS NOT NULL
                    ORDER BY dead_lettered_at, alert_id LIMIT %s
                    """,
                    (limit,),
                )
                rows = cursor.fetchall()
            return tuple(_decode_alert(*row) for row in rows)
        except ObservabilityStorageError:
            raise
        except Exception as exc:
            raise ObservabilityStorageError(
                "PostgreSQL dead-letter query failed"
            ) from exc

    def requeue(self, *, alert_id: str) -> bool:
        now = self._now()
        try:
            with self._connect() as conn, conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT dead_lettered_at, alert_json, checksum
                    FROM dataset_monitor_alert_outbox
                    WHERE alert_id = %s AND delivered_at IS NULL FOR UPDATE
                    """,
                    (alert_id,),
                )
                row = cursor.fetchone()
                if row is None:
                    raise AlertLeaseError("alert missing or already delivered")
                _decode_alert(row[1], row[2])
                if row[0] is None:
                    return False
                cursor.execute(
                    """
                    UPDATE dataset_monitor_alert_outbox
                    SET dead_lettered_at = NULL, attempt_count = 0,
                        next_attempt_at = NULL, last_reason_code = NULL
                    WHERE alert_id = %s
                    """,
                    (alert_id,),
                )
                self._event(
                    cursor, alert_id=alert_id,
                    event_type="requeued", attempts=0, now=now,
                )
                return True
        except (AlertLeaseError, ObservabilityStorageError):
            raise
        except Exception as exc:
            raise ObservabilityStorageError(
                "PostgreSQL alert requeue failed"
            ) from exc

    def delivery_events(
        self, *, alert_id: str
    ) -> tuple[tuple[str, int, str | None], ...]:
        try:
            with self._connect() as conn, conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT event_type, attempt_count, reason_code
                    FROM dataset_monitor_alert_delivery_events
                    WHERE alert_id = %s
                    ORDER BY event_seq
                    """,
                    (alert_id,),
                )
                rows = cursor.fetchall()
            return tuple((name, attempts, reason) for name, attempts, reason in rows)
        except Exception as exc:
            raise ObservabilityStorageError(
                "PostgreSQL alert audit query failed"
            ) from exc
