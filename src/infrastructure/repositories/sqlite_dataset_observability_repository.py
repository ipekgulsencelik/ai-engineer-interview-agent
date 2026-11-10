"""Transactional monitoring snapshots, durable alert outbox and delivery receipts."""

from __future__ import annotations

import hashlib
import json
import math
import sqlite3
from contextlib import closing
from datetime import UTC, datetime
from pathlib import Path

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


def _digest(payload: str) -> str:
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _decode_snapshot(payload: str, checksum: str) -> MonitoringSnapshot:
    if _digest(payload) != checksum:
        raise ObservabilityStorageError("monitoring snapshot checksum mismatch")
    try:
        value = json.loads(payload)
        if not isinstance(value, dict):
            raise ValueError("monitoring snapshot must be an object")
        return MonitoringSnapshotSerializer.deserialize(value)
    except (ValueError, KeyError, TypeError) as exc:
        raise ObservabilityStorageError("invalid monitoring snapshot data") from exc


def _decode_alert(payload: str, checksum: str) -> MonitoringAlert:
    if _digest(payload) != checksum:
        raise ObservabilityStorageError("alert outbox checksum mismatch")
    try:
        value = json.loads(payload)
        if not isinstance(value, dict):
            raise ValueError("alert payload must be an object")
        return alert_from_dict(value)
    except (ValueError, KeyError, TypeError) as exc:
        raise ObservabilityStorageError("invalid alert outbox data") from exc


class SQLiteDatasetObservabilityRepository:
    """Atomic append-only snapshots and separate at-least-once alert outbox."""

    def __init__(self, path: str | Path, *, timeout: float = 10.0) -> None:
        self._path = str(path)
        if not self._path.strip() or self._path == ":memory:":
            raise ObservabilityStorageError("storage requires a file-backed database")
        if (
            type(timeout) not in (int, float)
            or not math.isfinite(timeout)
            or timeout <= 0
        ):
            raise ObservabilityStorageError("timeout must be positive and finite")
        self._timeout = float(timeout)
        try:
            with closing(self._connect()) as conn, conn:
                conn.executescript(
                    """
                    CREATE TABLE IF NOT EXISTS dataset_monitor_snapshots (
                        monitor_run_id TEXT PRIMARY KEY,
                        dataset_id TEXT NOT NULL,
                        recorded_at TEXT NOT NULL,
                        payload_json TEXT NOT NULL,
                        checksum TEXT NOT NULL
                    );
                    CREATE INDEX IF NOT EXISTS ix_monitor_dataset_time
                      ON dataset_monitor_snapshots(dataset_id, recorded_at DESC);
                    CREATE TABLE IF NOT EXISTS dataset_monitor_alert_outbox (
                        alert_id TEXT PRIMARY KEY,
                        monitor_run_id TEXT NOT NULL,
                        alert_json TEXT NOT NULL,
                        checksum TEXT NOT NULL,
                        delivered_at TEXT,
                        FOREIGN KEY (monitor_run_id)
                          REFERENCES dataset_monitor_snapshots(monitor_run_id)
                    );
                    CREATE INDEX IF NOT EXISTS ix_monitor_pending_alerts
                      ON dataset_monitor_alert_outbox(delivered_at, alert_id);
                    CREATE TABLE IF NOT EXISTS dataset_monitor_alert_receipts (
                        alert_id TEXT PRIMARY KEY,
                        delivered_at TEXT NOT NULL,
                        FOREIGN KEY (alert_id)
                          REFERENCES dataset_monitor_alert_outbox(alert_id)
                    );
                    """
                )
        except sqlite3.DatabaseError as exc:
            raise ObservabilityStorageError(
                "monitoring store initialization failed"
            ) from exc

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._path, timeout=self._timeout)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def save(self, *, snapshot: MonitoringSnapshot) -> bool:
        """Write snapshot and all associated pending alerts in one transaction."""
        payload = canonical_json(MonitoringSnapshotSerializer.serialize(snapshot))
        checksum = _digest(payload)
        try:
            with closing(self._connect()) as conn, conn:
                conn.execute("BEGIN IMMEDIATE")
                previous = conn.execute(
                    """
                    SELECT payload_json, checksum FROM dataset_monitor_snapshots
                    WHERE monitor_run_id = ?
                    """, (snapshot.monitor_run_id,),
                ).fetchone()
                if previous is not None:
                    _decode_snapshot(previous[0], previous[1])
                    if previous != (payload, checksum):
                        raise ObservabilityStorageError(
                            "monitor_run_id already exists with different content"
                        )
                    return False
                conn.execute(
                    """
                    INSERT INTO dataset_monitor_snapshots
                      (monitor_run_id, dataset_id, recorded_at, payload_json, checksum)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        snapshot.monitor_run_id, snapshot.dataset_id,
                        snapshot.recorded_at.isoformat(), payload, checksum,
                    ),
                )
                for alert in snapshot.alerts:
                    value = canonical_json(alert_to_dict(alert))
                    conn.execute(
                        """
                        INSERT INTO dataset_monitor_alert_outbox
                        (alert_id, monitor_run_id, alert_json, checksum)
                        VALUES (?, ?, ?, ?)
                        """,
                        (
                            alert.alert_id, snapshot.monitor_run_id,
                            value, _digest(value),
                        ),
                    )
                return True
        except sqlite3.DatabaseError as exc:
            raise ObservabilityStorageError(
                "monitoring transaction failed"
            ) from exc

    def get(self, *, monitor_run_id: str) -> MonitoringSnapshot | None:
        try:
            with closing(self._connect()) as conn:
                row = conn.execute(
                    """
                    SELECT payload_json, checksum FROM dataset_monitor_snapshots
                    WHERE monitor_run_id = ?
                    """, (monitor_run_id,),
                ).fetchone()
        except sqlite3.DatabaseError as exc:
            raise ObservabilityStorageError("monitoring lookup failed") from exc
        return _decode_snapshot(*row) if row is not None else None

    def list_snapshots(
        self, *, dataset_id: str, limit: int = 100
    ) -> tuple[MonitoringSnapshot, ...]:
        if type(limit) is not int or not 1 <= limit <= 1000:
            raise ObservabilityStorageError("limit must be between 1 and 1000")
        try:
            with closing(self._connect()) as conn:
                rows = conn.execute(
                    """
                    SELECT payload_json, checksum FROM dataset_monitor_snapshots
                    WHERE dataset_id = ?
                    ORDER BY recorded_at DESC, monitor_run_id DESC LIMIT ?
                    """, (dataset_id, limit),
                ).fetchall()
        except sqlite3.DatabaseError as exc:
            raise ObservabilityStorageError("monitoring listing failed") from exc
        return tuple(_decode_snapshot(*row) for row in rows)

    def pending(self, *, limit: int = 100) -> tuple[MonitoringAlert, ...]:
        if type(limit) is not int or not 1 <= limit <= 1000:
            raise ObservabilityStorageError("limit must be between 1 and 1000")
        try:
            with closing(self._connect()) as conn:
                rows = conn.execute(
                    """
                    SELECT a.alert_json, a.checksum
                    FROM dataset_monitor_alert_outbox AS a
                    JOIN dataset_monitor_snapshots AS s
                      ON s.monitor_run_id = a.monitor_run_id
                    WHERE a.delivered_at IS NULL
                    ORDER BY s.recorded_at, a.alert_id LIMIT ?
                    """, (limit,),
                ).fetchall()
        except sqlite3.DatabaseError as exc:
            raise ObservabilityStorageError("alert outbox query failed") from exc
        return tuple(_decode_alert(*row) for row in rows)

    def mark_delivered(self, *, alert_id: str) -> bool:
        """Record receipt in the same transaction as changing delivery state."""
        try:
            with closing(self._connect()) as conn, conn:
                conn.execute("BEGIN IMMEDIATE")
                row = conn.execute(
                    """
                    SELECT delivered_at, alert_json, checksum
                    FROM dataset_monitor_alert_outbox WHERE alert_id = ?
                    """, (alert_id,),
                ).fetchone()
                if row is None:
                    raise ObservabilityStorageError("alert does not exist")
                _decode_alert(row[1], row[2])
                if row[0] is not None:
                    return False
                delivered_at = datetime.now(UTC).isoformat()
                conn.execute(
                    """
                    UPDATE dataset_monitor_alert_outbox SET delivered_at = ?
                    WHERE alert_id = ? AND delivered_at IS NULL
                    """, (delivered_at, alert_id),
                )
                conn.execute(
                    """
                    INSERT INTO dataset_monitor_alert_receipts
                    (alert_id, delivered_at) VALUES (?, ?)
                    """, (alert_id, delivered_at),
                )
                return True
        except sqlite3.DatabaseError as exc:
            raise ObservabilityStorageError(
                "alert delivery acknowledgment failed"
            ) from exc
