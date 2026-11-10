"""Atomic SQLite adapter for immutable dataset provenance DAGs."""

from __future__ import annotations

import sqlite3
from contextlib import closing
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

from src.evaluation.dataset.lineage.errors import (
    DatasetLineageError,
    LineageConflictError,
    LineageNotFoundError,
    LineageStorageError,
)
from src.evaluation.dataset.lineage.models import (
    DatasetLineageNode,
    DatasetRevision,
    LineageAuditEvent,
    LineageRegistration,
    LineageRelation,
    ParentLink,
)
from src.evaluation.dataset.lineage.services import validate_registration


class SQLiteDatasetLineageRepository:
    """Register complete provenance records in one SQLite transaction.

    A parent must have been committed before its child. As node identities
    are immutable, an edge can never introduce a directed cycle.
    """

    def __init__(self, path: str | Path, *, timeout: float = 10.0) -> None:
        self._path = str(path)
        if not self._path.strip() or self._path == ":memory:":
            raise DatasetLineageError(
                "lineage requires a file-backed SQLite database"
            )
        if not isinstance(timeout, (float, int)) or timeout <= 0:
            raise DatasetLineageError("timeout must be positive")
        self._timeout = float(timeout)
        try:
            with closing(self._connect()) as conn, conn:
                conn.executescript(
                    """
                    CREATE TABLE IF NOT EXISTS dataset_lineage_nodes (
                        dataset_id TEXT NOT NULL,
                        version TEXT NOT NULL,
                        content_sha256 TEXT NOT NULL,
                        producer TEXT NOT NULL,
                        created_at TEXT NOT NULL,
                        schema_version TEXT,
                        PRIMARY KEY (dataset_id, version)
                    );
                    CREATE TABLE IF NOT EXISTS dataset_lineage_edges (
                        child_id TEXT NOT NULL,
                        child_version TEXT NOT NULL,
                        parent_id TEXT NOT NULL,
                        parent_version TEXT NOT NULL,
                        relation TEXT NOT NULL,
                        PRIMARY KEY (
                            child_id, child_version, parent_id, parent_version
                        ),
                        FOREIGN KEY (child_id, child_version)
                            REFERENCES dataset_lineage_nodes(dataset_id, version),
                        FOREIGN KEY (parent_id, parent_version)
                            REFERENCES dataset_lineage_nodes(dataset_id, version)
                    );
                    CREATE INDEX IF NOT EXISTS ix_dataset_lineage_edges_parent
                        ON dataset_lineage_edges (parent_id, parent_version);
                    CREATE TABLE IF NOT EXISTS dataset_lineage_audit (
                        event_id TEXT PRIMARY KEY,
                        dataset_id TEXT NOT NULL,
                        version TEXT NOT NULL,
                        content_sha256 TEXT NOT NULL,
                        parent_count INTEGER NOT NULL,
                        occurred_at TEXT NOT NULL,
                        UNIQUE (dataset_id, version),
                        FOREIGN KEY (dataset_id, version)
                            REFERENCES dataset_lineage_nodes(dataset_id, version)
                    );
                    """
                )
        except sqlite3.DatabaseError as exc:
            raise LineageStorageError(
                "could not initialize dataset lineage storage"
            ) from exc

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self._path, timeout=self._timeout)
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    @staticmethod
    def _node_values(node: DatasetLineageNode) -> tuple[str, ...]:
        return (
            node.content_sha256,
            node.producer,
            node.created_at.isoformat(),
            node.schema_version or "",
        )

    @staticmethod
    def _load_node(
        conn: sqlite3.Connection,
        revision: DatasetRevision,
    ) -> tuple[str, str, str, str] | None:
        result = conn.execute(
            """
            SELECT content_sha256, producer, created_at,
                   COALESCE(schema_version, '')
            FROM dataset_lineage_nodes
            WHERE dataset_id = ? AND version = ?
            """,
            (revision.dataset_id, revision.version),
        ).fetchone()
        return result

    @staticmethod
    def _load_links(
        conn: sqlite3.Connection,
        revision: DatasetRevision,
    ) -> tuple[tuple[str, str, str], ...]:
        rows = conn.execute(
            """
            SELECT parent_id, parent_version, relation
            FROM dataset_lineage_edges
            WHERE child_id = ? AND child_version = ?
            ORDER BY parent_id, parent_version, relation
            """,
            (revision.dataset_id, revision.version),
        ).fetchall()
        return tuple(rows)

    @staticmethod
    def _load_event(
        conn: sqlite3.Connection,
        revision: DatasetRevision,
    ) -> LineageAuditEvent:
        result = conn.execute(
            """
            SELECT event_id, content_sha256, parent_count, occurred_at
            FROM dataset_lineage_audit
            WHERE dataset_id = ? AND version = ?
            """,
            (revision.dataset_id, revision.version),
        ).fetchone()
        if result is None:
            raise LineageStorageError("lineage audit is missing for revision")
        return LineageAuditEvent(
            event_id=result[0],
            revision=revision,
            content_sha256=result[1],
            parent_count=result[2],
            occurred_at=datetime.fromisoformat(result[3]),
        )

    def register(
        self,
        *,
        node: DatasetLineageNode,
        parents: tuple[ParentLink, ...],
    ) -> LineageRegistration:
        validate_registration(node=node, parents=parents)
        links = tuple(
            sorted(
                (
                    link.parent.dataset_id,
                    link.parent.version,
                    link.relation.value,
                )
                for link in parents
            )
        )
        try:
            with closing(self._connect()) as conn, conn:
                conn.execute("BEGIN IMMEDIATE")
                existing = self._load_node(conn, node.revision)
                if existing is not None:
                    if (
                        existing != self._node_values(node)
                        or self._load_links(conn, node.revision) != links
                    ):
                        raise LineageConflictError(
                            "dataset revision already exists with different provenance"
                        )
                    return LineageRegistration(
                        created=False,
                        event=self._load_event(conn, node.revision),
                    )

                for link in parents:
                    if self._load_node(conn, link.parent) is None:
                        raise LineageNotFoundError(
                            "a parent dataset revision is not registered"
                        )
                conn.execute(
                    """
                    INSERT INTO dataset_lineage_nodes (
                        dataset_id, version, content_sha256, producer,
                        created_at, schema_version
                    ) VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        node.revision.dataset_id,
                        node.revision.version,
                        node.content_sha256,
                        node.producer,
                        node.created_at.isoformat(),
                        node.schema_version,
                    ),
                )
                for parent_id, parent_version, relation in links:
                    conn.execute(
                        """
                        INSERT INTO dataset_lineage_edges (
                            child_id, child_version, parent_id,
                            parent_version, relation
                        ) VALUES (?, ?, ?, ?, ?)
                        """,
                        (
                            node.revision.dataset_id,
                            node.revision.version,
                            parent_id,
                            parent_version,
                            relation,
                        ),
                    )
                event = LineageAuditEvent(
                    event_id=uuid4().hex,
                    revision=node.revision,
                    content_sha256=node.content_sha256,
                    parent_count=len(parents),
                    occurred_at=datetime.now(UTC),
                )
                conn.execute(
                    """
                    INSERT INTO dataset_lineage_audit (
                        event_id, dataset_id, version, content_sha256,
                        parent_count, occurred_at
                    ) VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        event.event_id,
                        node.revision.dataset_id,
                        node.revision.version,
                        event.content_sha256,
                        event.parent_count,
                        event.occurred_at.isoformat(),
                    ),
                )
                return LineageRegistration(created=True, event=event)
        except sqlite3.DatabaseError as exc:
            raise LineageStorageError(
                "dataset lineage registration transaction failed"
            ) from exc

    def get_node(
        self, *, revision: DatasetRevision
    ) -> DatasetLineageNode | None:
        try:
            with closing(self._connect()) as conn:
                stored = self._load_node(conn, revision)
        except sqlite3.DatabaseError as exc:
            raise LineageStorageError("lineage node lookup failed") from exc
        if stored is None:
            return None
        return DatasetLineageNode(
            revision=revision,
            content_sha256=stored[0],
            producer=stored[1],
            created_at=datetime.fromisoformat(stored[2]),
            schema_version=stored[3] or None,
        )

    def get_parents(
        self, *, revision: DatasetRevision
    ) -> tuple[ParentLink, ...]:
        try:
            with closing(self._connect()) as conn:
                if self._load_node(conn, revision) is None:
                    raise LineageNotFoundError("dataset revision not found")
                rows = self._load_links(conn, revision)
        except sqlite3.DatabaseError as exc:
            raise LineageStorageError("lineage parent lookup failed") from exc
        return tuple(
            ParentLink(
                parent=DatasetRevision(
                    dataset_id=parent_id,
                    version=parent_version,
                ),
                relation=LineageRelation(relation),
            )
            for parent_id, parent_version, relation in rows
        )

    def get_children(
        self, *, revision: DatasetRevision
    ) -> tuple[DatasetRevision, ...]:
        try:
            with closing(self._connect()) as conn:
                if self._load_node(conn, revision) is None:
                    raise LineageNotFoundError("dataset revision not found")
                rows = conn.execute(
                    """
                    SELECT child_id, child_version FROM dataset_lineage_edges
                    WHERE parent_id = ? AND parent_version = ?
                    ORDER BY child_id, child_version
                    """,
                    (revision.dataset_id, revision.version),
                ).fetchall()
        except sqlite3.DatabaseError as exc:
            raise LineageStorageError("lineage child lookup failed") from exc
        return tuple(
            DatasetRevision(dataset_id=dataset_id, version=version)
            for dataset_id, version in rows
        )

    def get_events(
        self, *, revision: DatasetRevision
    ) -> tuple[LineageAuditEvent, ...]:
        try:
            with closing(self._connect()) as conn:
                if self._load_node(conn, revision) is None:
                    raise LineageNotFoundError("dataset revision not found")
                event = self._load_event(conn, revision)
        except sqlite3.DatabaseError as exc:
            raise LineageStorageError("lineage audit lookup failed") from exc
        return (event,)
