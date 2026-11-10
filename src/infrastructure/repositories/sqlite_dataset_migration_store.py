"""Transactional SQLite snapshots with durable migration and rollback audit."""

from __future__ import annotations

import hashlib
import json
import sqlite3
from contextlib import closing
from collections.abc import Mapping, Sequence
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

from src.evaluation.dataset.schema_evolution.errors import SchemaEvolutionError
from src.evaluation.dataset.schema_evolution.models import parse_schema_version
from src.evaluation.dataset.schema_evolution.persistence import (
    MigrationAuditEvent,
    MigrationSnapshot,
)


def _encode_records(records: Sequence[Mapping[str, object]]) -> str:
    try:
        return json.dumps(
            [dict(record) for record in records],
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise SchemaEvolutionError("records must be JSON-serializable") from exc


def _hash(encoded: str) -> str:
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def _event(row: tuple[Any, ...]) -> MigrationAuditEvent:
    return MigrationAuditEvent(
        event_id=row[0],
        schema_name=row[1],
        operation=row[2],
        source_version=row[3],
        target_version=row[4],
        source_hash=row[5],
        target_hash=row[6],
        record_count=row[7],
        occurred_at=datetime.fromisoformat(row[8]),
    )


class SQLiteDatasetMigrationStore:
    """Atomic snapshot switching; audit and records commit in one transaction."""

    def __init__(self, path: str | Path) -> None:
        self._path = str(path)
        with closing(sqlite3.connect(self._path)) as conn, conn:
            conn.execute("PRAGMA foreign_keys = ON")
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS dataset_migration_snapshots (
                    snapshot_id TEXT PRIMARY KEY,
                    schema_name TEXT NOT NULL,
                    schema_version TEXT NOT NULL,
                    records_json TEXT NOT NULL,
                    checksum TEXT NOT NULL,
                    previous_id TEXT REFERENCES dataset_migration_snapshots(snapshot_id),
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS dataset_migration_heads (
                    schema_name TEXT PRIMARY KEY,
                    snapshot_id TEXT NOT NULL
                        REFERENCES dataset_migration_snapshots(snapshot_id)
                );
                CREATE TABLE IF NOT EXISTS dataset_migration_audit (
                    event_id TEXT PRIMARY KEY,
                    schema_name TEXT NOT NULL,
                    operation TEXT NOT NULL,
                    source_version TEXT NOT NULL,
                    target_version TEXT NOT NULL,
                    source_hash TEXT NOT NULL,
                    target_hash TEXT NOT NULL,
                    record_count INTEGER NOT NULL,
                    occurred_at TEXT NOT NULL
                );
                """
            )

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._path)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def _add_snapshot(
        self,
        conn: sqlite3.Connection,
        *,
        schema_name: str,
        schema_version: str,
        records_json: str,
        previous_id: str | None,
    ) -> str:
        snapshot_id = uuid4().hex
        conn.execute(
            """
            INSERT INTO dataset_migration_snapshots
            (snapshot_id, schema_name, schema_version, records_json,
             checksum, previous_id, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                snapshot_id,
                schema_name,
                schema_version,
                records_json,
                _hash(records_json),
                previous_id,
                datetime.now(UTC).isoformat(),
            ),
        )
        return snapshot_id

    def _record_audit(
        self,
        conn: sqlite3.Connection,
        *,
        schema_name: str,
        operation: str,
        source_version: str,
        target_version: str,
        source_hash: str,
        target_hash: str,
        record_count: int,
    ) -> MigrationAuditEvent:
        entry = MigrationAuditEvent(
            event_id=uuid4().hex,
            schema_name=schema_name,
            operation=operation,
            source_version=source_version,
            target_version=target_version,
            source_hash=source_hash,
            target_hash=target_hash,
            record_count=record_count,
            occurred_at=datetime.now(UTC),
        )
        conn.execute(
            """
            INSERT INTO dataset_migration_audit
            (event_id, schema_name, operation, source_version, target_version,
             source_hash, target_hash, record_count, occurred_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                entry.event_id, entry.schema_name, entry.operation,
                entry.source_version, entry.target_version, entry.source_hash,
                entry.target_hash, entry.record_count, entry.occurred_at.isoformat(),
            ),
        )
        return entry

    def _head(
        self, conn: sqlite3.Connection, *, schema_name: str
    ) -> tuple[str, str, str, str, str | None] | None:
        row = conn.execute(
            """
            SELECT s.snapshot_id, s.schema_version, s.records_json,
                   s.checksum, s.previous_id
            FROM dataset_migration_heads AS h
            JOIN dataset_migration_snapshots AS s
              ON s.snapshot_id = h.snapshot_id
            WHERE h.schema_name = ?
            """,
            (schema_name,),
        ).fetchone()
        return row

    def commit_migration(
        self,
        *,
        schema_name: str,
        source_version: str,
        target_version: str,
        source_records: Sequence[Mapping[str, object]],
        target_records: Sequence[Mapping[str, object]],
    ) -> MigrationAuditEvent:
        if parse_schema_version(target_version) <= parse_schema_version(
            source_version
        ):
            raise SchemaEvolutionError(
                "persisted migration target version must increase"
            )
        if len(source_records) != len(target_records):
            raise SchemaEvolutionError("migration must preserve record count")
        original = _encode_records(source_records)
        migrated = _encode_records(target_records)
        try:
            with closing(self._connect()) as conn, conn:
                conn.execute("BEGIN IMMEDIATE")
                head = self._head(conn, schema_name=schema_name)
                if head is None:
                    previous_id = self._add_snapshot(
                        conn,
                        schema_name=schema_name,
                        schema_version=source_version,
                        records_json=original,
                        previous_id=None,
                    )
                else:
                    previous_id, version, _records_json, checksum, _parent = head
                    if version != source_version or checksum != _hash(original):
                        raise SchemaEvolutionError(
                            "active dataset differs from expected source snapshot"
                        )
                target_id = self._add_snapshot(
                    conn,
                    schema_name=schema_name,
                    schema_version=target_version,
                    records_json=migrated,
                    previous_id=previous_id,
                )
                conn.execute(
                    """
                    INSERT INTO dataset_migration_heads (schema_name, snapshot_id)
                    VALUES (?, ?)
                    ON CONFLICT(schema_name)
                    DO UPDATE SET snapshot_id=excluded.snapshot_id
                    """,
                    (schema_name, target_id),
                )
                return self._record_audit(
                    conn,
                    schema_name=schema_name,
                    operation="migration",
                    source_version=source_version,
                    target_version=target_version,
                    source_hash=_hash(original),
                    target_hash=_hash(migrated),
                    record_count=len(target_records),
                )
        except sqlite3.DatabaseError as exc:
            raise SchemaEvolutionError("migration transaction failed") from exc

    def rollback_last(self, *, schema_name: str) -> MigrationAuditEvent:
        try:
            with closing(self._connect()) as conn, conn:
                conn.execute("BEGIN IMMEDIATE")
                head = self._head(conn, schema_name=schema_name)
                if head is None or head[4] is None:
                    raise SchemaEvolutionError("no migration to roll back")
                parent = conn.execute(
                    """
                    SELECT schema_version, records_json, checksum
                    FROM dataset_migration_snapshots WHERE snapshot_id = ?
                    """,
                    (head[4],),
                ).fetchone()
                if parent is None:
                    raise SchemaEvolutionError("previous snapshot is missing")
                conn.execute(
                    """
                    UPDATE dataset_migration_heads SET snapshot_id = ?
                    WHERE schema_name = ?
                    """,
                    (head[4], schema_name),
                )
                return self._record_audit(
                    conn,
                    schema_name=schema_name,
                    operation="rollback",
                    source_version=head[1],
                    target_version=parent[0],
                    source_hash=head[3],
                    target_hash=parent[2],
                    record_count=len(json.loads(parent[1])),
                )
        except sqlite3.DatabaseError as exc:
            raise SchemaEvolutionError("rollback transaction failed") from exc

    def current_snapshot(self, *, schema_name: str) -> MigrationSnapshot | None:
        try:
            with closing(self._connect()) as conn, conn:
                head = self._head(conn, schema_name=schema_name)
        except sqlite3.DatabaseError as exc:
            raise SchemaEvolutionError("migration snapshot read failed") from exc
        if head is None:
            return None
        if _hash(head[2]) != head[3]:
            raise SchemaEvolutionError("snapshot checksum mismatch")
        return MigrationSnapshot(
            schema_name=schema_name,
            schema_version=head[1],
            records=tuple(json.loads(head[2])),
            checksum=head[3],
        )

    def audit_events(self, *, schema_name: str) -> tuple[MigrationAuditEvent, ...]:
        try:
            with closing(self._connect()) as conn, conn:
                rows = conn.execute(
                    """
                    SELECT event_id, schema_name, operation, source_version,
                           target_version, source_hash, target_hash,
                           record_count, occurred_at
                    FROM dataset_migration_audit WHERE schema_name = ?
                    ORDER BY rowid
                    """,
                    (schema_name,),
                ).fetchall()
        except sqlite3.DatabaseError as exc:
            raise SchemaEvolutionError("migration audit read failed") from exc
        return tuple(_event(row) for row in rows)
