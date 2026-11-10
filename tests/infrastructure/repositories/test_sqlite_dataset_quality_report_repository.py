"""Durable, idempotent and corruption-detecting quality report tests."""

from __future__ import annotations

import sqlite3
from concurrent.futures import ThreadPoolExecutor

import pytest

from src.evaluation.dataset.quality import (
    DatasetQualityCoordinator,
    DatasetQualityEngine,
    QualityReportStorageError,
    RequiredFieldRule,
)
from src.infrastructure.repositories.sqlite_dataset_quality_report_repository import (
    SQLiteDatasetQualityReportRepository,
)


def _report():
    return DatasetQualityEngine(
        record_rules=(RequiredFieldRule(field_path="id"),),
        id_factory=lambda: "report-1",
    ).evaluate(
        dataset_id="interview-dataset",
        dataset_version="1.0.0",
        records=[{"id": "a"}, {}],
    )


def test_quality_report_round_trip_survives_restart(tmp_path) -> None:
    path = tmp_path / "quality.sqlite"
    store = SQLiteDatasetQualityReportRepository(path)
    report = _report()
    assert store.save(report=report)
    restored = SQLiteDatasetQualityReportRepository(path)
    assert restored.get(run_id="report-1") == report
    assert restored.list_reports(dataset_id="interview-dataset") == (report,)
    assert restored.get(run_id="does-not-exist") is None


def test_exact_retry_is_idempotent_and_conflicts_fail(tmp_path) -> None:
    store = SQLiteDatasetQualityReportRepository(tmp_path / "quality.sqlite")
    report = _report()
    assert store.save(report=report)
    assert not store.save(report=report)
    changed = DatasetQualityEngine(
        record_rules=(RequiredFieldRule(field_path="id"),),
        id_factory=lambda: "report-1",
    ).evaluate(
        dataset_id="interview-dataset",
        dataset_version="1.0.0",
        records=[{"id": "a"}],
    )
    with pytest.raises(QualityReportStorageError, match="different report"):
        store.save(report=changed)
    assert store.get(run_id="report-1") == report


def test_corruption_detected_on_read_and_retry(tmp_path) -> None:
    path = tmp_path / "quality.sqlite"
    store = SQLiteDatasetQualityReportRepository(path)
    report = _report()
    store.save(report=report)
    with sqlite3.connect(path) as conn:
        conn.execute(
            """
            UPDATE dataset_quality_reports SET report_json = '{}'
            WHERE run_id = ?
            """,
            (report.run_id,),
        )
    with pytest.raises(QualityReportStorageError, match="checksum"):
        store.get(run_id=report.run_id)
    with pytest.raises(QualityReportStorageError, match="checksum"):
        store.save(report=report)


def test_failed_insert_rolls_back_without_partial_rows(tmp_path) -> None:
    path = tmp_path / "quality.sqlite"
    store = SQLiteDatasetQualityReportRepository(path)
    with sqlite3.connect(path) as conn:
        conn.execute(
            """
            CREATE TRIGGER reject_reports
            BEFORE INSERT ON dataset_quality_reports
            BEGIN SELECT RAISE(ABORT, 'injected failure'); END
            """
        )
    with pytest.raises(QualityReportStorageError, match="transaction"):
        store.save(report=_report())
    assert store.list_reports(dataset_id="interview-dataset") == ()


def test_concurrent_retry_stores_exactly_one_report(tmp_path) -> None:
    path = tmp_path / "quality.sqlite"
    store = SQLiteDatasetQualityReportRepository(path)
    report = _report()
    with ThreadPoolExecutor(max_workers=6) as pool:
        results = list(
            pool.map(
                lambda _i: store.save(report=report),
                range(6),
            )
        )
    assert sum(results) == 1
    assert store.list_reports(dataset_id="interview-dataset") == (report,)


def test_bounded_listing_and_invalid_limits(tmp_path) -> None:
    store = SQLiteDatasetQualityReportRepository(tmp_path / "quality.sqlite")
    store.save(report=_report())
    assert len(store.list_reports(dataset_id="interview-dataset", limit=1)) == 1
    for invalid in (0, 1001, True):
        with pytest.raises(QualityReportStorageError, match="limit"):
            store.list_reports(
                dataset_id="interview-dataset", limit=invalid
            )


def test_coordinator_persists_failed_quality_gates(tmp_path) -> None:
    store = SQLiteDatasetQualityReportRepository(tmp_path / "quality.sqlite")
    evaluator = DatasetQualityEngine(
        record_rules=(RequiredFieldRule(field_path="id"),),
        id_factory=lambda: "failed-quality-1",
    )
    coordinator = DatasetQualityCoordinator(evaluator=evaluator, store=store)
    report = coordinator.evaluate_and_store(
        dataset_id="interview-dataset",
        dataset_version="1.0.0",
        records=[{}],
    )
    assert not report.accepted
    assert store.get(run_id="failed-quality-1") == report


def test_repository_rejects_memory_database() -> None:
    with pytest.raises(QualityReportStorageError, match="file-backed"):
        SQLiteDatasetQualityReportRepository(":memory:")


def test_report_storage_does_not_persist_raw_record_content(tmp_path) -> None:
    path = tmp_path / "quality.sqlite"
    store = SQLiteDatasetQualityReportRepository(path)
    report = DatasetQualityEngine(
        record_rules=(RequiredFieldRule(field_path="id"),),
        id_factory=lambda: "privacy-test",
    ).evaluate(
        dataset_id="test",
        dataset_version="1.0.0",
        records=[{"id": None, "private_answer": "NEVER-STORE-RAW-SAMPLE-2026"}],
    )
    store.save(report=report)
    assert b"NEVER-STORE-RAW-SAMPLE-2026" not in path.read_bytes()
