"""Behavioral contracts for persisted, registry-scoped quality scoring."""

from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime, timedelta

import pytest

from src.evaluation.dataset.lineage.models import DatasetRevision
from src.evaluation.dataset.quality.models import (
    IssueSeverity,
    QualityIssue,
    QualityReport,
)
from src.evaluation.dataset.quality.scoring import (
    SCORE_MODEL_VERSION,
    DatasetQualityScoringError,
    DatasetQualityScoringService,
    QualityScoreCalculator,
    QualityScoringPolicy,
)
from src.evaluation.dataset.registry.models import DatasetCatalogEntry
from src.evaluation.dataset.schema_evolution.models import parse_schema_version
from src.infrastructure.repositories.sqlite_dataset_quality_report_repository import (
    SQLiteDatasetQualityReportRepository,
)


def _report(
    version: str = "1.0.0",
    *,
    run_id: str = "run-a",
    bad: bool = False,
    accepted: bool = True,
    day: int = 1,
) -> QualityReport:
    issues = (
        (
            QualityIssue(
                rule_id="required-id",
                code="missing",
                message="Sensitive value must not appear in score output",
                severity=IssueSeverity.ERROR,
                record_index=0,
            ),
        )
        if bad
        else ()
    )
    return QualityReport(
        run_id=run_id,
        dataset_id="interview-qa",
        dataset_version=version,
        checked_at=datetime(2026, 11, 1, tzinfo=UTC) + timedelta(days=day),
        record_count=2,
        total_checks=2,
        passed_checks=1 if bad else 2,
        failed_checks=1 if bad else 0,
        error_count=1 if bad else 0,
        warning_count=0,
        failed_record_count=1 if bad else 0,
        pass_rate=0.5 if bad else 1.0,
        accepted=accepted,
        issues=issues,
    )


class MemoryHistory:
    def __init__(self, reports: tuple[QualityReport, ...]) -> None:
        self.reports = reports

    def list_reports(
        self, *, dataset_id: str, limit: int = 100
    ) -> tuple[QualityReport, ...]:
        return self.reports[:limit]


class Registry:
    def __init__(self, versions: tuple[str, ...]) -> None:
        self.entries = {
            version: DatasetCatalogEntry(
                revision=DatasetRevision(
                    dataset_id="interview-qa", version=version
                ),
                content_sha256="0" * 64,
                producer="test",
                created_at=datetime(2026, 11, 1, tzinfo=UTC),
                name="Test dataset",
                owner_id="test-team",
            )
            for version in versions
        }

    def get(self, *, revision: DatasetRevision) -> DatasetCatalogEntry | None:
        return self.entries.get(revision.version)

    def list_versions(
        self, *, dataset_id: str, limit: int = 100
    ) -> tuple[DatasetCatalogEntry, ...]:
        ordered = sorted(self.entries, key=parse_schema_version, reverse=True)
        return tuple(self.entries[version] for version in ordered[:limit])


def _service(
    reports: tuple[QualityReport, ...],
    *,
    policy: QualityScoringPolicy | None = None,
    versions: tuple[str, ...] | None = None,
) -> DatasetQualityScoringService:
    return DatasetQualityScoringService(
        history=MemoryHistory(reports),
        registry=Registry(
            versions
            if versions is not None
            else tuple(report.dataset_version for report in reports)
        ),
        policy=policy,
    )


def test_healthy_registered_dataset_scores_100_without_false_baseline() -> None:
    report = _report()
    result = _service((report,)).score_run(
        dataset_id="interview-qa", run_id=report.run_id
    )
    assert result.score_model_version == SCORE_MODEL_VERSION
    assert (result.check_points, result.record_points, result.severity_points) == (
        70.0, 20.0, 10.0
    )
    assert result.score == 100.0
    assert result.passed
    assert result.baseline_version is None
    assert result.reason_codes == ()


def test_error_density_and_failed_records_produce_explainable_score() -> None:
    report = _report(bad=True, accepted=True)
    result = _service(
        (report,), policy=QualityScoringPolicy(min_score=0.0)
    ).score_run(dataset_id="interview-qa", run_id="run-a")
    assert result.score == 50.0
    assert (result.check_points, result.record_points, result.severity_points) == (
        35.0, 10.0, 5.0
    )
    assert result.passed
    assert not hasattr(result, "issues")
    assert not hasattr(result, "message")


def test_rule_gate_failure_remains_blocking_even_with_low_score_threshold() -> None:
    report = _report(bad=True, accepted=False)
    result = _service(
        (report,), policy=QualityScoringPolicy(min_score=0)
    ).score_run(dataset_id="interview-qa", run_id="run-a")
    assert not result.passed
    assert result.reason_codes == ("quality_rules_rejected",)


def test_numeric_semver_history_and_regression_gate() -> None:
    old = _report("1.9.0", run_id="old", day=1)
    baseline = _report("1.10.0", run_id="baseline", day=2)
    candidate = _report("2.0.0", run_id="new", bad=True, day=3)
    service = _service(
        (candidate, old, baseline),
        policy=QualityScoringPolicy(
            min_score=0, max_regression_points=5
        ),
    )
    rows = service.score_versions(dataset_id="interview-qa")
    assert [row.dataset_version for row in rows] == [
        "1.9.0", "1.10.0", "2.0.0"
    ]
    result = service.score_run(dataset_id="interview-qa", run_id="new")
    assert result.baseline_version == "1.10.0"
    assert result.baseline_score == 100.0
    assert result.regression_points == 50.0
    assert not result.passed
    assert result.reason_codes == ("quality_regression",)


def test_latest_run_per_version_selected_by_timestamp_and_tie_breaker() -> None:
    first = _report("1.0.0", run_id="a", day=2, bad=True)
    second = _report("1.0.0", run_id="b", day=2)
    later = _report("2.0.0", run_id="next", day=3)
    result = _service((later, first, second)).score_versions(
        dataset_id="interview-qa"
    )
    assert len(result) == 2
    assert result[0].run_id == "b"
    assert result[1].baseline_score == 100.0


def test_missing_intermediate_registered_version_report_blocks_gate() -> None:
    old = _report("1.0.0", run_id="old", day=1)
    current = _report("1.2.0", run_id="new", day=2)
    result = _service(
        (current, old), versions=("1.0.0", "1.1.0", "1.2.0")
    ).score_run(dataset_id="interview-qa", run_id="new")
    assert not result.passed
    assert result.baseline_version == "1.1.0"
    assert result.baseline_score is None
    assert result.reason_codes == ("baseline_report_missing",)


def test_truncated_catalog_versions_fail_closed() -> None:
    report = _report("1.1.0")
    service = _service(
        (report,),
        versions=("1.0.0", "1.1.0"),
        policy=QualityScoringPolicy(history_limit=2),
    )
    with pytest.raises(DatasetQualityScoringError, match="catalog window"):
        service.score_versions(dataset_id="interview-qa")


def test_rejected_baseline_prevents_unsafe_regression_comparison() -> None:
    old = _report("1.0.0", accepted=False)
    current = _report("1.1.0", run_id="current", day=2)
    result = _service((current, old)).score_run(
        dataset_id="interview-qa", run_id="current"
    )
    assert not result.passed
    assert result.reason_codes == ("baseline_rules_rejected",)


def test_missing_baseline_can_be_required() -> None:
    report = _report()
    service = _service(
        (report,), policy=QualityScoringPolicy(require_baseline=True)
    )
    result = service.score_run(dataset_id="interview-qa", run_id="run-a")
    assert not result.passed
    assert result.reason_codes == ("baseline_missing",)


def test_missing_registered_version_fails_closed() -> None:
    with pytest.raises(DatasetQualityScoringError, match="unregistered"):
        _service((_report(),), versions=()).score_versions(
            dataset_id="interview-qa"
        )


def test_truncated_history_cannot_hide_earlier_baselines() -> None:
    reports = (
        _report("1.1.0", run_id="new"),
        _report("1.0.0", run_id="old"),
    )
    with pytest.raises(DatasetQualityScoringError, match="truncated"):
        _service(
            reports, policy=QualityScoringPolicy(history_limit=2)
        ).score_versions(dataset_id="interview-qa")


def test_duplicate_run_or_wrong_dataset_identity_is_rejected() -> None:
    report = _report()
    with pytest.raises(DatasetQualityScoringError, match="duplicate"):
        _service((report, report)).score_versions(dataset_id="interview-qa")
    with pytest.raises(DatasetQualityScoringError, match="identity"):
        _service((replace(report, dataset_id="different"),)).score_versions(
            dataset_id="interview-qa"
        )


def test_empty_report_and_unchecked_report_score_zero() -> None:
    report = _report()
    empty = replace(
        report,
        record_count=0,
        total_checks=0,
        passed_checks=0,
        failed_checks=0,
        pass_rate=0.0,
    )
    assert QualityScoreCalculator.score(empty) == 0.0


@pytest.mark.parametrize(
    "kwargs",
    [
        {"min_score": True},
        {"min_score": float("nan")},
        {"min_score": 101},
        {"max_regression_points": -1},
        {"max_regression_points": float("inf")},
        {"require_baseline": 1},
        {"history_limit": 1},
        {"history_limit": True},
        {"history_limit": 1001},
    ],
)
def test_invalid_scoring_policy_is_rejected(kwargs: dict) -> None:
    with pytest.raises(DatasetQualityScoringError):
        QualityScoringPolicy(**kwargs)


def test_invalid_request_and_unknown_run_are_rejected() -> None:
    service = _service((_report(),))
    with pytest.raises(DatasetQualityScoringError, match="run_id"):
        service.score_run(dataset_id="interview-qa", run_id="")
    with pytest.raises(DatasetQualityScoringError, match="run_id"):
        service.score_run(dataset_id="interview-qa", run_id="no-such-run")
    with pytest.raises(DatasetQualityScoringError, match="dataset_id"):
        service.score_versions(dataset_id="")


def test_durable_sqlite_reports_support_scoring_after_restart(tmp_path) -> None:
    path = tmp_path / "quality.sqlite"
    writer = SQLiteDatasetQualityReportRepository(path)
    old = _report("1.0.0", run_id="old", day=1)
    new = _report("1.1.0", run_id="new", day=2, bad=True)
    assert writer.save(report=old)
    assert writer.save(report=new)
    reader = SQLiteDatasetQualityReportRepository(path)
    service = DatasetQualityScoringService(
        history=reader,
        registry=Registry(("1.0.0", "1.1.0")),
        policy=QualityScoringPolicy(min_score=0),
    )
    scores = service.score_versions(dataset_id="interview-qa")
    assert [(item.dataset_version, item.score) for item in scores] == [
        ("1.0.0", 100.0),
        ("1.1.0", 50.0),
    ]
    assert not scores[-1].passed
    assert scores[-1].reason_codes == ("quality_regression",)
