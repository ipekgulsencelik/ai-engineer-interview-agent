"""Transactional SQLite catalog for immutable dataset versions and tags."""

from __future__ import annotations

import hashlib
import json
import math
import re
import sqlite3
from contextlib import closing
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

from src.evaluation.dataset.lineage.models import DatasetRevision
from src.evaluation.dataset.registry.errors import (
    DatasetRegistryConflictError,
    DatasetRegistryError,
    DatasetRegistryStorageError,
)
from src.evaluation.dataset.registry.models import DatasetCatalogEntry
from src.evaluation.dataset.schema_evolution.models import parse_schema_version

_TAG = re.compile(r"[a-z0-9][a-z0-9._-]{0,63}")


def _serialize(entry: DatasetCatalogEntry) -> str:
    """Stable catalog metadata encoding; never include sample payloads."""
    return json.dumps(
        {
            "dataset_id": entry.revision.dataset_id,
            "version": entry.revision.version,
            "content_sha256": entry.content_sha256,
            "producer": entry.producer,
            "created_at": entry.created_at.isoformat(),
            "name": entry.name,
            "owner_id": entry.owner_id,
            "schema_version": entry.schema_version,
            "tags": list(entry.tags),
            "description": entry.description,
        },
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def _checksum(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def _validate_limit(limit: int) -> None:
    if type(limit) is not int or not 1 <= limit <= 1000:
        raise DatasetRegistryError("limit must be between 1 and 1000")


class SQLiteDatasetRegistryRepository:
    """A write-once local catalog; readers verify JSON and tag projections.

    Version monotonicity, the metadata row, its tags, and its audit event
    are protected by a single BEGIN IMMEDIATE write transaction.
    """

    def __init__(self, path: str | Path, *, timeout: float = 10.0) -> None:
        self._path = str(path)
        if not self._path.strip() or self._path == ":memory:":
            raise DatasetRegistryError("registry requires file-backed SQLite")
        if (
            type(timeout) not in (int, float)
            or not math.isfinite(timeout)
            or timeout <= 0
        ):
            raise DatasetRegistryError("timeout must be finite and positive")
        self._timeout = float(timeout)
        try:
            with closing(self._connect()) as conn, conn:
                conn.executescript(
                    """
                    CREATE TABLE IF NOT EXISTS dataset_registry_entries (
                        dataset_id TEXT NOT NULL,
                        version TEXT NOT NULL,
                        version_major INTEGER NOT NULL,
                        version_minor INTEGER NOT NULL,
                        version_patch INTEGER NOT NULL,
                        entry_json TEXT NOT NULL,
                        checksum TEXT NOT NULL,
                        PRIMARY KEY (dataset_id, version),
                        UNIQUE (
                            dataset_id, version_major,
                            version_minor, version_patch
                        )
                    );
                    CREATE INDEX IF NOT EXISTS ix_dataset_registry_latest
                        ON dataset_registry_entries (
                            dataset_id, version_major DESC,
                            version_minor DESC, version_patch DESC
                        );
                    CREATE TABLE IF NOT EXISTS dataset_registry_tags (
                        dataset_id TEXT NOT NULL,
                        version TEXT NOT NULL,
                        tag TEXT NOT NULL,
                        PRIMARY KEY (dataset_id, version, tag),
                        FOREIGN KEY (dataset_id, version)
                            REFERENCES dataset_registry_entries(dataset_id, version)
                    );
                    CREATE INDEX IF NOT EXISTS ix_dataset_registry_tags
                        ON dataset_registry_tags (tag, dataset_id, version);
                    CREATE TABLE IF NOT EXISTS dataset_registry_audit (
                        event_id TEXT PRIMARY KEY,
                        dataset_id TEXT NOT NULL,
                        version TEXT NOT NULL,
                        content_sha256 TEXT NOT NULL,
                        occurred_at TEXT NOT NULL,
                        UNIQUE (dataset_id, version),
                        FOREIGN KEY (dataset_id, version)
                            REFERENCES dataset_registry_entries(dataset_id, version)
                    );
                    """
                )
        except sqlite3.DatabaseError as exc:
            raise DatasetRegistryStorageError(
                "could not initialize dataset registry"
            ) from exc

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._path, timeout=self._timeout)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    @staticmethod
    def _decode(
        conn: sqlite3.Connection,
        row: tuple[str, str, int, int, int, str, str],
    ) -> DatasetCatalogEntry:
        dataset_id, version, major, minor, patch, content, digest = row
        if _checksum(content) != digest:
            raise DatasetRegistryStorageError(
                "dataset registry checksum mismatch"
            )
        try:
            payload = json.loads(content)
            if not isinstance(payload, dict):
                raise ValueError("stored entry is not an object")
            raw_tags = payload["tags"]
            if not isinstance(raw_tags, list):
                raise ValueError("stored tags are not a list")
            entry = DatasetCatalogEntry(
                revision=DatasetRevision(
                    dataset_id=payload["dataset_id"],
                    version=payload["version"],
                ),
                content_sha256=payload["content_sha256"],
                producer=payload["producer"],
                created_at=datetime.fromisoformat(payload["created_at"]),
                name=payload["name"],
                owner_id=payload["owner_id"],
                schema_version=payload["schema_version"],
                tags=tuple(raw_tags),
                description=payload["description"],
            )
            if (major, minor, patch) != parse_schema_version(version):
                raise ValueError("stored semantic version index differs")
            if entry.revision.dataset_id != dataset_id:
                raise ValueError("stored dataset identity differs")
            if entry.revision.version != version:
                raise ValueError("stored version differs")
            if _serialize(entry) != content:
                raise ValueError("stored metadata is not canonical")
            tag_rows = conn.execute(
                """
                SELECT tag FROM dataset_registry_tags
                WHERE dataset_id = ? AND version = ? ORDER BY tag
                """,
                (dataset_id, version),
            ).fetchall()
            if tuple(item[0] for item in tag_rows) != entry.tags:
                raise ValueError("stored tag index differs")
            audit = conn.execute(
                """
                SELECT event_id, content_sha256, occurred_at
                FROM dataset_registry_audit
                WHERE dataset_id = ? AND version = ?
                """,
                (dataset_id, version),
            ).fetchone()
            if audit is None or not isinstance(audit[0], str) or not audit[0]:
                raise ValueError("dataset registry audit event is missing")
            if audit[1] != entry.content_sha256:
                raise ValueError("dataset registry audit content digest differs")
            occurred_at = datetime.fromisoformat(audit[2])
            if occurred_at.tzinfo is None or occurred_at.utcoffset() is None:
                raise ValueError("dataset registry audit timestamp is naive")
            return entry
        except (KeyError, TypeError, ValueError, OverflowError) as exc:
            raise DatasetRegistryStorageError(
                "dataset registry entry is invalid"
            ) from exc

    def register(self, *, entry: DatasetCatalogEntry) -> bool:
        """Return False for an exact replay; reject stale and conflicting writes."""
        if not isinstance(entry, DatasetCatalogEntry):
            raise DatasetRegistryError("entry must be DatasetCatalogEntry")
        revision = entry.revision
        version = parse_schema_version(revision.version)
        content = _serialize(entry)
        digest = _checksum(content)
        try:
            with closing(self._connect()) as conn, conn:
                conn.execute("BEGIN IMMEDIATE")
                rows = conn.execute(
                    """
                    SELECT dataset_id, version, version_major, version_minor,
                           version_patch, entry_json, checksum
                    FROM dataset_registry_entries WHERE dataset_id = ?
                    """,
                    (revision.dataset_id,),
                ).fetchall()
                # Validate every persisted version and its auxiliary projections
                # before relying on either metadata or denormalized indexes.
                registered = tuple(self._decode(conn, row) for row in rows)
                for persisted in registered:
                    if persisted.revision.version != revision.version:
                        continue
                    if persisted != entry:
                        raise DatasetRegistryConflictError(
                            "revision already registered with different metadata"
                        )
                    return False
                if registered and version <= max(
                    parse_schema_version(item.revision.version)
                    for item in registered
                ):
                    raise DatasetRegistryConflictError(
                        "new dataset version must be greater than latest"
                    )
                conn.execute(
                    """
                    INSERT INTO dataset_registry_entries (
                        dataset_id, version, version_major, version_minor,
                        version_patch, entry_json, checksum
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (revision.dataset_id, revision.version, *version, content, digest),
                )
                conn.executemany(
                    """
                    INSERT INTO dataset_registry_tags(dataset_id, version, tag)
                    VALUES (?, ?, ?)
                    """,
                    [
                        (revision.dataset_id, revision.version, tag)
                        for tag in entry.tags
                    ],
                )
                conn.execute(
                    """
                    INSERT INTO dataset_registry_audit (
                        event_id, dataset_id, version, content_sha256, occurred_at
                    ) VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        uuid4().hex,
                        revision.dataset_id,
                        revision.version,
                        entry.content_sha256,
                        datetime.now(UTC).isoformat(),
                    ),
                )
                return True
        except sqlite3.DatabaseError as exc:
            raise DatasetRegistryStorageError(
                "dataset registry transaction failed"
            ) from exc

    def get(self, *, revision: DatasetRevision) -> DatasetCatalogEntry | None:
        if not isinstance(revision, DatasetRevision):
            raise DatasetRegistryError("revision must be DatasetRevision")
        try:
            with closing(self._connect()) as conn:
                row = conn.execute(
                    """
                    SELECT dataset_id, version, version_major, version_minor,
                           version_patch, entry_json, checksum
                    FROM dataset_registry_entries
                    WHERE dataset_id = ? AND version = ?
                    """,
                    (revision.dataset_id, revision.version),
                ).fetchone()
                return self._decode(conn, row) if row is not None else None
        except sqlite3.DatabaseError as exc:
            raise DatasetRegistryStorageError(
                "dataset registry lookup failed"
            ) from exc

    def list_versions(
        self, *, dataset_id: str, limit: int = 100
    ) -> tuple[DatasetCatalogEntry, ...]:
        _validate_limit(limit)
        DatasetRevision(dataset_id=dataset_id, version="0.0.0")
        try:
            with closing(self._connect()) as conn:
                rows = conn.execute(
                    """
                    SELECT dataset_id, version, version_major, version_minor,
                           version_patch, entry_json, checksum
                    FROM dataset_registry_entries WHERE dataset_id = ?
                    """,
                    (dataset_id,),
                ).fetchall()
                entries = tuple(self._decode(conn, row) for row in rows)
                ordered = sorted(
                    entries,
                    key=lambda item: parse_schema_version(item.revision.version),
                    reverse=True,
                )
                return tuple(ordered[:limit])
        except sqlite3.DatabaseError as exc:
            raise DatasetRegistryStorageError(
                "dataset registry version listing failed"
            ) from exc

    def list_by_tag(
        self, *, tag: str, limit: int = 100
    ) -> tuple[DatasetCatalogEntry, ...]:
        _validate_limit(limit)
        if not isinstance(tag, str) or _TAG.fullmatch(tag) is None:
            raise DatasetRegistryError("tag must be a lowercase identifier")
        try:
            with closing(self._connect()) as conn:
                # Scan and validate canonical entries, not the tag index:
                # a deleted tag row otherwise silently hides its owner.
                rows = conn.execute(
                    """
                    SELECT dataset_id, version, version_major, version_minor,
                           version_patch, entry_json, checksum
                    FROM dataset_registry_entries
                    """
                ).fetchall()
                entries = tuple(self._decode(conn, row) for row in rows)
                tagged = (item for item in entries if tag in item.tags)
                ordered = sorted(
                    tagged,
                    key=lambda item: (
                        item.revision.dataset_id,
                        *(
                            -part
                            for part in parse_schema_version(item.revision.version)
                        ),
                    ),
                )
                return tuple(ordered[:limit])
        except sqlite3.DatabaseError as exc:
            raise DatasetRegistryStorageError(
                "dataset registry tag listing failed"
            ) from exc
