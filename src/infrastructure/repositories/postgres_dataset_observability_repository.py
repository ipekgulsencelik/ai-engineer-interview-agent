"""PostgreSQL adapter for atomic monitoring snapshots and alert creation."""

from __future__ import annotations

import hashlib
import json

from src.evaluation.dataset.observability.errors import ObservabilityStorageError
from src.evaluation.dataset.observability.models import (
    MonitoringAlert,
    MonitoringSnapshot,
)
from src.evaluation.dataset.observability.serialization import (
    MonitoringSnapshotSerializer,
    alert_from_dict,
    alert_to_dict,
    canonical_json,
)
from src.infrastructure.repositories.postgres_connection import (
    PostgresConnectionPort,
)


def _digest(payload: str) -> str:
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _decode_snapshot(payload: str, checksum: str) -> MonitoringSnapshot:
    if _digest(payload) != checksum:
        raise ObservabilityStorageError("monitoring snapshot checksum mismatch")
    try:
        data = json.loads(payload)
        if not isinstance(data, dict):
            raise ValueError("expected object")
        return MonitoringSnapshotSerializer.deserialize(data)
    except (ValueError, KeyError, TypeError) as exc:
        raise ObservabilityStorageError("invalid monitoring snapshot") from exc


def _decode_alert(payload: str, checksum: str) -> MonitoringAlert:
    if _digest(payload) != checksum:
        raise ObservabilityStorageError("alert checksum mismatch")
    try:
        data = json.loads(payload)
        if not isinstance(data, dict):
            raise ValueError("expected object")
        return alert_from_dict(data)
    except (ValueError, KeyError, TypeError) as exc:
        raise ObservabilityStorageError("invalid stored alert") from exc


class PostgresDatasetObservabilityRepository:
    """Port-compatible writer/reader; Alembic owns schema creation."""

    def __init__(self, *, connect: PostgresConnectionPort) -> None:
        self._connect = connect

    def save(self, *, snapshot: MonitoringSnapshot) -> bool:
        content = canonical_json(MonitoringSnapshotSerializer.serialize(snapshot))
        checksum = _digest(content)
        # Preserve domain failures and redact connection errors: DSNs may be
        # present in transport exception messages.
        try:
            with self._connect() as conn, conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO dataset_monitor_snapshots
                        (monitor_run_id, dataset_id, recorded_at,
                         payload_json, checksum)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (monitor_run_id) DO NOTHING
                    RETURNING monitor_run_id
                    """,
                    (
                        snapshot.monitor_run_id,
                        snapshot.dataset_id,
                        snapshot.recorded_at,
                        content,
                        checksum,
                    ),
                )
                created = cursor.fetchone() is not None
                if created:
                    for alert in snapshot.alerts:
                        value = canonical_json(alert_to_dict(alert))
                        cursor.execute(
                            """
                            INSERT INTO dataset_monitor_alert_outbox
                                (alert_id, monitor_run_id, alert_json, checksum)
                            VALUES (%s, %s, %s, %s)
                            """,
                            (
                                alert.alert_id,
                                snapshot.monitor_run_id,
                                value,
                                _digest(value),
                            ),
                        )
                    return True
                cursor.execute(
                    """
                    SELECT payload_json, checksum FROM dataset_monitor_snapshots
                    WHERE monitor_run_id = %s
                    """,
                    (snapshot.monitor_run_id,),
                )
                row = cursor.fetchone()
                if row is None:
                    raise ObservabilityStorageError(
                        "conflicting monitoring snapshot disappeared"
                    )
                _decode_snapshot(row[0], row[1])
                if tuple(row) != (content, checksum):
                    raise ObservabilityStorageError(
                        "monitor_run_id already exists with different content"
                    )
                return False
        except ObservabilityStorageError:
            raise
        except Exception as exc:
            raise ObservabilityStorageError(
                "PostgreSQL monitoring transaction failed"
            ) from exc

    def get(self, *, monitor_run_id: str) -> MonitoringSnapshot | None:
        try:
            with self._connect() as conn, conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT payload_json, checksum FROM dataset_monitor_snapshots
                    WHERE monitor_run_id = %s
                    """,
                    (monitor_run_id,),
                )
                row = cursor.fetchone()
            return _decode_snapshot(*row) if row else None
        except ObservabilityStorageError:
            raise
        except Exception as exc:
            raise ObservabilityStorageError(
                "PostgreSQL monitoring lookup failed"
            ) from exc

    def list_snapshots(
        self, *, dataset_id: str, limit: int = 100
    ) -> tuple[MonitoringSnapshot, ...]:
        if type(limit) is not int or not 1 <= limit <= 1000:
            raise ObservabilityStorageError("limit must be in [1, 1000]")
        try:
            with self._connect() as conn, conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT payload_json, checksum FROM dataset_monitor_snapshots
                    WHERE dataset_id = %s
                    ORDER BY recorded_at DESC, monitor_run_id DESC
                    LIMIT %s
                    """,
                    (dataset_id, limit),
                )
                rows = cursor.fetchall()
            return tuple(_decode_snapshot(*row) for row in rows)
        except ObservabilityStorageError:
            raise
        except Exception as exc:
            raise ObservabilityStorageError(
                "PostgreSQL monitoring listing failed"
            ) from exc
