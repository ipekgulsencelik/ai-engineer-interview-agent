"""Deterministic v1 scores and regression gates from durable quality reports.

Scores are derived metadata, not measurements of factual answer accuracy.
No raw records, issue messages, or external provider dependencies are used.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

from src.evaluation.dataset.lineage.models import DatasetRevision
from src.evaluation.dataset.quality.models import QualityReport
from src.evaluation.dataset.registry.ports import RegistryReader
from src.evaluation.dataset.schema_evolution.models import parse_schema_version

SCORE_MODEL_VERSION = "dataset-quality-v1"


class DatasetQualityScoringError(ValueError):
    """The scoring policy or trusted history is incomplete or inconsistent."""


@dataclass(frozen=True, slots=True, kw_only=True)
class QualityScoringPolicy:
    """Scoring thresholds; independent of the underlying quality rule policy."""

    min_score: float = 90.0
    max_regression_points: float = 5.0
    require_baseline: bool = False
    history_limit: int = 1000

    def __post_init__(self) -> None:
        for name in ("min_score", "max_regression_points"):
            value = getattr(self, name)
            if (
                type(value) not in (int, float)
                or not math.isfinite(value)
                or not 0 <= value <= 100
            ):
                raise DatasetQualityScoringError(
                    f"{name} must be finite and between 0 and 100"
                )
        if type(self.require_baseline) is not bool:
            raise DatasetQualityScoringError("require_baseline must be boolean")
        if type(self.history_limit) is not int or not 2 <= self.history_limit <= 1000:
            raise DatasetQualityScoringError("history_limit must be 2..1000")


@dataclass(frozen=True, slots=True, kw_only=True)
class DatasetQualityScore:
    """Explainable score for one persisted quality-report run."""

    score_model_version: str
    dataset_id: str
    dataset_version: str
    run_id: str
    checked_at: datetime
    score: float
    check_points: float
    record_points: float
    severity_points: float
    quality_rules_accepted: bool
    baseline_version: str | None
    baseline_score: float | None
    regression_points: float | None
    passed: bool
    reason_codes: tuple[str, ...]


class QualityReportHistoryPort(Protocol):
    """Read-only boundary implemented by the existing SQLite quality report store."""

    def list_reports(
        self, *, dataset_id: str, limit: int = 100
    ) -> tuple[QualityReport, ...]: ...


class QualityScoreCalculator:
    """Stable v1 formula: checks 70, record success 20, error density 10."""

    @staticmethod
    def components(report: QualityReport) -> tuple[float, float, float]:
        if not isinstance(report, QualityReport):
            raise DatasetQualityScoringError("report must be QualityReport")
        if report.record_count == 0 or report.total_checks == 0:
            return (0.0, 0.0, 0.0)
        check_points = 70.0 * report.pass_rate
        record_points = 20.0 * (
            1.0 - report.failed_record_count / report.record_count
        )
        error_density = min(1.0, report.error_count / report.total_checks)
        severity_points = 10.0 * (1.0 - error_density)
        return (
            round(check_points, 2),
            round(record_points, 2),
            round(severity_points, 2),
        )

    @classmethod
    def score(cls, report: QualityReport) -> float:
        return round(sum(cls.components(report)), 2)


class DatasetQualityScoringService:
    """Read existing reports, verify registry identity, and evaluate version gates.

    No writes occur. Source reports remain authoritative and immutable.
    """

    def __init__(
        self,
        *,
        history: QualityReportHistoryPort,
        registry: RegistryReader,
        policy: QualityScoringPolicy | None = None,
    ) -> None:
        self._history = history
        self._registry = registry
        self._policy = policy if policy is not None else QualityScoringPolicy()

    def score_run(
        self, *, dataset_id: str, run_id: str
    ) -> DatasetQualityScore:
        if not isinstance(run_id, str) or not run_id.strip():
            raise DatasetQualityScoringError("run_id must be non-empty")
        reports = self._read_history(dataset_id=dataset_id)
        target = next((report for report in reports if report.run_id == run_id), None)
        if target is None:
            raise DatasetQualityScoringError("run_id is not in bounded history")
        versions = self._catalog_versions(dataset_id=dataset_id)
        prior_version = self._previous_version(
            versions=versions, current=target.dataset_version
        )
        baseline = next(
            (item for item in self._latest_by_version(reports)
             if item.dataset_version == prior_version),
            None,
        )
        return self._decision(
            report=target, baseline=baseline, expected_baseline=prior_version
        )

    def score_versions(
        self, *, dataset_id: str
    ) -> tuple[DatasetQualityScore, ...]:
        """Return one latest-run score per SemVer, oldest version first."""
        reports = self._read_history(dataset_id=dataset_id)
        versions = self._catalog_versions(dataset_id=dataset_id)
        ordered = self._latest_by_version(reports)
        by_version = {report.dataset_version: report for report in ordered}
        output: list[DatasetQualityScore] = []
        for report in ordered:
            prior_version = self._previous_version(
                versions=versions, current=report.dataset_version
            )
            output.append(
                self._decision(
                    report=report,
                    baseline=by_version.get(prior_version),
                    expected_baseline=prior_version,
                )
            )
        return tuple(output)

    def _read_history(self, *, dataset_id: str) -> tuple[QualityReport, ...]:
        if (
            not isinstance(dataset_id, str)
            or not dataset_id.strip()
            or len(dataset_id) > 128
        ):
            raise DatasetQualityScoringError("dataset_id must be 1..128 chars")
        reports = self._history.list_reports(
            dataset_id=dataset_id, limit=self._policy.history_limit
        )
        if not isinstance(reports, tuple):
            raise DatasetQualityScoringError("history must be a report tuple")
        # A full page may hide an earlier baseline: do not silently compare
        # against an incomplete window. Cursor pagination is a future increment.
        if len(reports) >= self._policy.history_limit:
            raise DatasetQualityScoringError("history window may be truncated")
        seen: set[str] = set()
        registered: set[str] = set()
        for report in reports:
            if not isinstance(report, QualityReport) or report.dataset_id != dataset_id:
                raise DatasetQualityScoringError("history report identity mismatch")
            if report.run_id in seen:
                raise DatasetQualityScoringError("duplicate quality run_id")
            seen.add(report.run_id)
            parse_schema_version(report.dataset_version)
            if report.dataset_version not in registered:
                revision = DatasetRevision(
                    dataset_id=dataset_id, version=report.dataset_version
                )
                if self._registry.get(revision=revision) is None:
                    raise DatasetQualityScoringError(
                        "quality history references unregistered revision"
                    )
                registered.add(report.dataset_version)
        return reports

    def _catalog_versions(self, *, dataset_id: str) -> tuple[str, ...]:
        entries = self._registry.list_versions(
            dataset_id=dataset_id, limit=self._policy.history_limit
        )
        if not isinstance(entries, tuple):
            raise DatasetQualityScoringError("catalog versions must be a tuple")
        if len(entries) >= self._policy.history_limit:
            raise DatasetQualityScoringError("catalog window may be truncated")
        versions: set[str] = set()
        for entry in entries:
            if entry.revision.dataset_id != dataset_id:
                raise DatasetQualityScoringError("catalog dataset identity mismatch")
            version = entry.revision.version
            parse_schema_version(version)
            if version in versions:
                raise DatasetQualityScoringError("duplicate catalog version")
            versions.add(version)
        return tuple(sorted(versions, key=parse_schema_version))

    @staticmethod
    def _previous_version(
        *, versions: tuple[str, ...], current: str
    ) -> str | None:
        if current not in versions:
            raise DatasetQualityScoringError(
                "quality report version missing from catalog"
            )
        predecessors = [
            version for version in versions
            if parse_schema_version(version) < parse_schema_version(current)
        ]
        return predecessors[-1] if predecessors else None

    @staticmethod
    def _latest_by_version(
        reports: tuple[QualityReport, ...]
    ) -> tuple[QualityReport, ...]:
        latest: dict[str, QualityReport] = {}
        for report in reports:
            old = latest.get(report.dataset_version)
            if old is None or (report.checked_at, report.run_id) > (
                old.checked_at, old.run_id
            ):
                latest[report.dataset_version] = report
        return tuple(
            sorted(
                latest.values(),
                key=lambda item: parse_schema_version(item.dataset_version),
            )
        )

    def _decision(
        self,
        *,
        report: QualityReport,
        baseline: QualityReport | None,
        expected_baseline: str | None,
    ) -> DatasetQualityScore:
        check, record, severity = QualityScoreCalculator.components(report)
        score = round(check + record + severity, 2)
        baseline_score = (
            QualityScoreCalculator.score(baseline) if baseline is not None else None
        )
        regression = (
            round(max(0.0, baseline_score - score), 2)
            if baseline_score is not None
            else None
        )
        reasons: list[str] = []
        if not report.accepted:
            reasons.append("quality_rules_rejected")
        if score < self._policy.min_score:
            reasons.append("score_below_threshold")
        if baseline is None:
            if expected_baseline is not None:
                reasons.append("baseline_report_missing")
            elif self._policy.require_baseline:
                reasons.append("baseline_missing")
        else:
            if not baseline.accepted:
                reasons.append("baseline_rules_rejected")
            if (
                regression is not None
                and regression > self._policy.max_regression_points
            ):
                reasons.append("quality_regression")
        return DatasetQualityScore(
            score_model_version=SCORE_MODEL_VERSION,
            dataset_id=report.dataset_id,
            dataset_version=report.dataset_version,
            run_id=report.run_id,
            checked_at=report.checked_at,
            score=score,
            check_points=check,
            record_points=record,
            severity_points=severity,
            quality_rules_accepted=report.accepted,
            baseline_version=expected_baseline,
            baseline_score=baseline_score,
            regression_points=regression,
            passed=not reasons,
            reason_codes=tuple(reasons),
        )
