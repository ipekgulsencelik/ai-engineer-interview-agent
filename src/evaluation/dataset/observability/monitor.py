"""Interpret existing quality reports and drift snapshots into alert signals."""

from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime
from typing import Protocol
from uuid import uuid4

from src.evaluation.dataset.observability.errors import DatasetObservabilityError
from src.evaluation.dataset.observability.models import (
    AlertSeverity,
    MonitoringAlert,
    MonitoringPolicy,
    MonitoringSnapshot,
    MonitoringStatus,
)
from src.evaluation.dataset.quality.models import QualityReport
from src.evaluation.dataset.services.dataset_drift_analyzer import (
    DatasetDriftAnalyzer,
)
from src.evaluation.dataset.value_objects.dataset_distribution_snapshot import (
    DatasetDistributionSnapshot,
)
from src.evaluation.dataset.value_objects.dataset_drift_snapshot import (
    DatasetDriftSnapshot,
)


class DriftAnalyzerPort(Protocol):
    def analyze(
        self,
        *,
        baseline: DatasetDistributionSnapshot,
        comparison: DatasetDistributionSnapshot,
        drift_threshold: float = 0.10,
        notes: str | None = None,
    ) -> DatasetDriftSnapshot: ...


class MonitoringClock(Protocol):
    def now(self) -> datetime: ...


class UTCMonitoringClock:
    def now(self) -> datetime:
        return datetime.now(UTC)


class DatasetObservabilityMonitor:
    """Compute metadata-only alerts; does not persist, send or log anything."""

    def __init__(
        self,
        *,
        policy: MonitoringPolicy | None = None,
        analyzer: DriftAnalyzerPort | None = None,
        clock: MonitoringClock | None = None,
        id_factory: Callable[[], str] | None = None,
    ) -> None:
        self._policy = policy if policy is not None else MonitoringPolicy()
        self._analyzer = analyzer if analyzer is not None else DatasetDriftAnalyzer()
        self._clock = clock if clock is not None else UTCMonitoringClock()
        self._id_factory = id_factory if id_factory is not None else lambda: uuid4().hex

    def evaluate(
        self,
        *,
        baseline_distribution: DatasetDistributionSnapshot,
        comparison_distribution: DatasetDistributionSnapshot,
        baseline_quality: QualityReport,
        comparison_quality: QualityReport,
    ) -> MonitoringSnapshot:
        self._validate_inputs(
            baseline_distribution=baseline_distribution,
            comparison_distribution=comparison_distribution,
            baseline_quality=baseline_quality,
            comparison_quality=comparison_quality,
        )
        drift = self._analyzer.analyze(
            baseline=baseline_distribution,
            comparison=comparison_distribution,
            drift_threshold=self._policy.drift_warning,
        )
        if (
            drift.baseline_dataset_id != baseline_distribution.dataset_id
            or drift.comparison_dataset_id != comparison_distribution.dataset_id
        ):
            raise DatasetObservabilityError("drift analyzer returned wrong dataset IDs")
        drift_score = drift.overall_drift_score
        pass_rate_drop = max(
            0.0, baseline_quality.pass_rate - comparison_quality.pass_rate
        )
        run_id = self._id_factory()
        alerts: list[MonitoringAlert] = []

        def append(
            code: str,
            severity: AlertSeverity,
            metric: str,
            observed: float,
            threshold: float,
        ) -> None:
            alerts.append(
                MonitoringAlert(
                    alert_id=f"{run_id}:{code}",
                    code=code,
                    severity=severity,
                    metric=metric,
                    observed=observed,
                    threshold=threshold,
                )
            )

        if not comparison_quality.accepted:
            append(
                "QUALITY_GATE_REJECTED", AlertSeverity.CRITICAL,
                "quality_accepted", 0.0, 1.0,
            )

        if (
            comparison_distribution.sample_count
            < self._policy.min_comparison_records
        ):
            append(
                "INSUFFICIENT_SAMPLES", AlertSeverity.CRITICAL,
                "sample_sufficiency_ratio",
                comparison_distribution.sample_count
                / self._policy.min_comparison_records,
                1.0,
            )

        if drift_score >= self._policy.drift_critical:
            append(
                "DRIFT_CRITICAL", AlertSeverity.CRITICAL,
                "distribution_drift", drift_score, self._policy.drift_critical,
            )
        elif drift_score >= self._policy.drift_warning:
            append(
                "DRIFT_WARNING", AlertSeverity.WARNING,
                "distribution_drift", drift_score, self._policy.drift_warning,
            )

        if pass_rate_drop >= self._policy.pass_rate_drop_critical:
            append(
                "QUALITY_REGRESSION_CRITICAL", AlertSeverity.CRITICAL,
                "pass_rate_drop", pass_rate_drop,
                self._policy.pass_rate_drop_critical,
            )
        elif pass_rate_drop >= self._policy.pass_rate_drop_warning:
            append(
                "QUALITY_REGRESSION_WARNING", AlertSeverity.WARNING,
                "pass_rate_drop", pass_rate_drop,
                self._policy.pass_rate_drop_warning,
            )

        status = (
            MonitoringStatus.CRITICAL
            if any(x.severity is AlertSeverity.CRITICAL for x in alerts)
            else MonitoringStatus.WARNING if alerts else MonitoringStatus.HEALTHY
        )
        return MonitoringSnapshot(
            monitor_run_id=run_id,
            dataset_id=comparison_distribution.dataset_id,
            dataset_version=comparison_quality.dataset_version,
            baseline_dataset_id=baseline_distribution.dataset_id,
            baseline_dataset_version=baseline_quality.dataset_version,
            baseline_quality_run_id=baseline_quality.run_id,
            comparison_quality_run_id=comparison_quality.run_id,
            recorded_at=self._clock.now(),
            record_count=comparison_distribution.sample_count,
            baseline_pass_rate=baseline_quality.pass_rate,
            comparison_pass_rate=comparison_quality.pass_rate,
            pass_rate_drop=pass_rate_drop,
            drift_score=drift_score,
            status=status,
            policy=self._policy,
            alerts=tuple(alerts),
        )

    @staticmethod
    def _validate_inputs(
        *,
        baseline_distribution: DatasetDistributionSnapshot,
        comparison_distribution: DatasetDistributionSnapshot,
        baseline_quality: QualityReport,
        comparison_quality: QualityReport,
    ) -> None:
        for distribution, quality in (
            (baseline_distribution, baseline_quality),
            (comparison_distribution, comparison_quality),
        ):
            if distribution.dataset_id != quality.dataset_id:
                raise DatasetObservabilityError("distribution and report dataset differ")
            if distribution.sample_count != quality.record_count:
                raise DatasetObservabilityError("distribution and quality counts differ")
            if distribution.sample_count < 1 or quality.total_checks < 1:
                raise DatasetObservabilityError(
                    "monitoring requires nonempty checked datasets"
                )
            for name in (
                "category_distribution", "level_distribution",
                "split_distribution",
            ):
                counts = getattr(distribution, name)
                if sum(counts.values()) != distribution.sample_count:
                    raise DatasetObservabilityError(
                        f"{name} counts do not match dataset sample_count"
                    )
        if baseline_quality.run_id == comparison_quality.run_id:
            raise DatasetObservabilityError("baseline and comparison runs must differ")
        if baseline_quality.checked_at > comparison_quality.checked_at:
            raise DatasetObservabilityError(
                "baseline quality report must not be newer than comparison"
            )
