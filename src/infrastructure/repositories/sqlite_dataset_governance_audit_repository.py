"""File-backed append-only audit events for catalog metadata access."""

from __future__ import annotations

import hashlib
import json
import sqlite3
from contextlib import closing
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from src.evaluation.dataset.governance import (
    CatalogAccessAuditEvent,
    DatasetGovernanceError,
)


def _encode(event: CatalogAccessAuditEvent) -> str:
    return json.dumps(
        {
            "event_id": event.event_id,
            "principal_id": event.principal_id,
            "tenant_id": event.tenant_id,
            "dataset_id": event.dataset_id,
            "version": event.version,
            "occurred_at": event.occurred_at.isoformat(),
            "allowed": event.allowed,
            "reason_code": event.reason_code,
        },
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def _digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _utc_sort_key(occurred_at: datetime) -> str:
    """Lexicographically sortable, uniform UTC timestamp with microseconds."""
    return occurred_at.astimezone(UTC).isoformat(timespec="microseconds")


class SQLiteDatasetGovernanceAuditRepository:
    """Local append-only audit, not a tamper-proof external audit ledger."""

    def __init__(self, path: str | Path, *, timeout: float = 10.0) -> None:
        self._path = str(path)
        if not self._path.strip() or self._path == ":memory:":
            raise DatasetGovernanceError("governance audit needs file-backed SQLite")
        if type(timeout) not in (int, float) or not 0 < timeout <= 60:
            raise DatasetGovernanceError("timeout must be in (0, 60]")
        self._timeout = float(timeout)
        try:
            with closing(self._connect()) as conn, conn:
                conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS dataset_catalog_access_events (
                        event_id TEXT PRIMARY KEY,
                        dataset_id TEXT NOT NULL,
                        occurred_at TEXT NOT NULL,
                        event_json TEXT NOT NULL,
                        checksum TEXT NOT NULL
                    )
                    """
                )
                conn.execute(
                    """
                    CREATE INDEX IF NOT EXISTS ix_dataset_catalog_access_events
                    ON dataset_catalog_access_events(dataset_id, occurred_at DESC)
                    """
                )
        except sqlite3.DatabaseError as exc:
            raise DatasetGovernanceError("could not initialize audit store") from exc

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self._path, timeout=self._timeout)

    def append(self, *, event: CatalogAccessAuditEvent) -> bool:
        if not isinstance(event, CatalogAccessAuditEvent):
            raise DatasetGovernanceError("audit event type is invalid")
        payload = _encode(event)
        try:
            with closing(self._connect()) as conn, conn:
                conn.execute("BEGIN IMMEDIATE")
                conn.execute(
                    """
                    INSERT INTO dataset_catalog_access_events(
                        event_id, dataset_id, occurred_at, event_json, checksum
                    ) VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        event.event_id,
                        event.dataset_id,
                        _utc_sort_key(event.occurred_at),
                        payload,
                        _digest(payload),
                    ),
                )
            return True
        except sqlite3.DatabaseError as exc:
            raise DatasetGovernanceError("could not append audit event") from exc

    @staticmethod
    def _decode(payload: str, checksum: str) -> CatalogAccessAuditEvent:
        if _digest(payload) != checksum:
            raise DatasetGovernanceError("audit checksum mismatch")
        try:
            data: Any = json.loads(payload)
            if not isinstance(data, dict):
                raise ValueError("audit payload must be an object")
            event = CatalogAccessAuditEvent(
                event_id=data["event_id"],
                principal_id=data["principal_id"],
                tenant_id=data["tenant_id"],
                dataset_id=data["dataset_id"],
                version=data["version"],
                occurred_at=datetime.fromisoformat(data["occurred_at"]),
                allowed=data["allowed"],
                reason_code=data["reason_code"],
            )
            if _encode(event) != payload:
                raise ValueError("noncanonical audit event")
            return event
        except (ValueError, TypeError, KeyError) as exc:
            raise DatasetGovernanceError("invalid stored audit event") from exc

    def list_events(
        self, *, dataset_id: str, limit: int = 100
    ) -> tuple[CatalogAccessAuditEvent, ...]:
        if not isinstance(dataset_id, str) or not dataset_id.strip():
            raise DatasetGovernanceError("dataset_id must be non-empty")
        if type(limit) is not int or not 1 <= limit <= 1000:
            raise DatasetGovernanceError("limit must be 1..1000")
        try:
            with closing(self._connect()) as conn:
                rows = conn.execute(
                    """
                    SELECT event_id, dataset_id, occurred_at, event_json, checksum
                    FROM dataset_catalog_access_events
                    WHERE dataset_id = ?
                    ORDER BY occurred_at DESC, event_id DESC
                    LIMIT ?
                    """,
                    (dataset_id, limit),
                ).fetchall()
        except sqlite3.DatabaseError as exc:
            raise DatasetGovernanceError("audit event query failed") from exc
        events = []
        for event_id, row_dataset, checked_at, payload, digest in rows:
            event = self._decode(payload, digest)
            if (
                event.event_id != event_id
                or event.dataset_id != row_dataset
                or _utc_sort_key(event.occurred_at) != checked_at
                or event.dataset_id != dataset_id
            ):
                raise DatasetGovernanceError("audit index and payload differ")
            events.append(event)
        return tuple(events)
