"""Transactional, immutable SQLite storage for dataset quality reports."""

from __future__ import annotations

import hashlib
import json
import sqlite3
from contextlib import closing
from pathlib import Path

from src.evaluation.dataset.quality.errors import QualityReportStorageError
from src.evaluation.dataset.quality.models import QualityReport
from src.evaluation.dataset.quality.reporting import QualityReportSerializer


def _encode(report: QualityReport) -> str:
    return json.dumps(
        QualityReportSerializer.serialize(report),
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
        ensure_ascii=False,
    )


def _sha256(payload: str) -> str:
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


class SQLiteDatasetQualityReportRepository:
    """Content-verifiable, write-once report store with concurrency safety."""

    def __init__(self, path: str | Path, *, timeout: float = 10.0) -> None:
        self._path = str(path)
        if not self._path.strip() or self._path == ":memory:":
            raise QualityReportStorageError(
                "quality reports require a file-backed SQLite database"
            )
        if (
            type(timeout) not in (float, int)
            or timeout <= 0
        ):
            raise QualityReportStorageError("timeout must be positive")
        self._timeout = float(timeout)
        try:
            with closing(self._connect()) as conn, conn:
                conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS dataset_quality_reports (
                        run_id TEXT PRIMARY KEY,
                        dataset_id TEXT NOT NULL,
                        dataset_version TEXT NOT NULL,
                        checked_at TEXT NOT NULL,
                        accepted INTEGER NOT NULL,
                        report_json TEXT NOT NULL,
                        checksum TEXT NOT NULL
                    )
                    """
                )
                conn.execute(
                    """
                    CREATE INDEX IF NOT EXISTS ix_dataset_quality_report_lookup
                    ON dataset_quality_reports(dataset_id, checked_at DESC)
                    """
                )
        except sqlite3.DatabaseError as exc:
            raise QualityReportStorageError(
                "could not initialize quality report storage"
            ) from exc

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self._path, timeout=self._timeout)

    def save(self, *, report: QualityReport) -> bool:
        """Return False for exact replay; never replace an existing run_id."""
        content = _encode(report)
        digest = _sha256(content)
        try:
            with closing(self._connect()) as conn, conn:
                conn.execute("BEGIN IMMEDIATE")
                existing = conn.execute(
                    """
                    SELECT report_json, checksum FROM dataset_quality_reports
                    WHERE run_id = ?
                    """,
                    (report.run_id,),
                ).fetchone()
                if existing is not None:
                    if _sha256(existing[0]) != existing[1]:
                        raise QualityReportStorageError(
                            "stored quality report checksum mismatch"
                        )
                    if existing[0] != content or existing[1] != digest:
                        raise QualityReportStorageError(
                            "run_id already exists with different report content"
                        )
                    return False
                conn.execute(
                    """
                    INSERT INTO dataset_quality_reports(
                        run_id, dataset_id, dataset_version,
                        checked_at, accepted, report_json, checksum
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        report.run_id,
                        report.dataset_id,
                        report.dataset_version,
                        report.checked_at.isoformat(),
                        int(report.accepted),
                        content,
                        digest,
                    ),
                )
                return True
        except sqlite3.DatabaseError as exc:
            raise QualityReportStorageError(
                "quality report storage transaction failed"
            ) from exc

    @staticmethod
    def _decode(content: str, digest: str) -> QualityReport:
        if _sha256(content) != digest:
            raise QualityReportStorageError(
                "stored quality report checksum mismatch"
            )
        try:
            payload = json.loads(content)
            if not isinstance(payload, dict):
                raise ValueError("stored report is not an object")
            return QualityReportSerializer.deserialize(payload)
        except (KeyError, TypeError, ValueError) as exc:
            raise QualityReportStorageError(
                "stored quality report is invalid"
            ) from exc

    def get(self, *, run_id: str) -> QualityReport | None:
        try:
            with closing(self._connect()) as conn:
                row = conn.execute(
                    """
                    SELECT report_json, checksum FROM dataset_quality_reports
                    WHERE run_id = ?
                    """,
                    (run_id,),
                ).fetchone()
        except sqlite3.DatabaseError as exc:
            raise QualityReportStorageError(
                "quality report lookup failed"
            ) from exc
        return self._decode(row[0], row[1]) if row is not None else None

    def list_reports(
        self, *, dataset_id: str, limit: int = 100
    ) -> tuple[QualityReport, ...]:
        if type(limit) is not int or not 1 <= limit <= 1000:
            raise QualityReportStorageError("limit must be between 1 and 1000")
        try:
            with closing(self._connect()) as conn:
                rows = conn.execute(
                    """
                    SELECT report_json, checksum FROM dataset_quality_reports
                    WHERE dataset_id = ?
                    ORDER BY checked_at DESC, run_id DESC
                    LIMIT ?
                    """,
                    (dataset_id, limit),
                ).fetchall()
        except sqlite3.DatabaseError as exc:
            raise QualityReportStorageError(
                "quality report listing failed"
            ) from exc
        return tuple(self._decode(content, digest) for content, digest in rows)
