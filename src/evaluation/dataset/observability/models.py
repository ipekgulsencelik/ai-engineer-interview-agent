"""Immutable monitoring, quality regression and alert contracts."""

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from src.evaluation.dataset.observability.errors import DatasetObservabilityError


def _unit(name: str, value: float) -> None:
    if (
        type(value) not in (int, float)
        or not math.isfinite(value)
        or not 0 <= value <= 1
    ):
        raise DatasetObservabilityError(f"{name} must be a finite [0, 1] number")


def _nonempty(name: str, value: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise DatasetObservabilityError(f"{name} must be a non-empty string")


class AlertSeverity(StrEnum):
    WARNING = "warning"
    CRITICAL = "critical"


class MonitoringStatus(StrEnum):
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"


@dataclass(frozen=True, slots=True, kw_only=True)
class MonitoringPolicy:
    drift_warning: float = 0.10
    drift_critical: float = 0.25
    pass_rate_drop_warning: float = 0.05
    pass_rate_drop_critical: float = 0.15
    min_comparison_records: int = 1

    def __post_init__(self) -> None:
        for name in (
            "drift_warning", "drift_critical",
            "pass_rate_drop_warning", "pass_rate_drop_critical",
        ):
            _unit(name, getattr(self, name))
        if self.drift_warning > self.drift_critical:
            raise DatasetObservabilityError(
                "drift_warning cannot exceed drift_critical"
            )
        if self.pass_rate_drop_warning > self.pass_rate_drop_critical:
            raise DatasetObservabilityError(
                "pass_rate_drop_warning cannot exceed pass_rate_drop_critical"
            )
        if (
            type(self.min_comparison_records) is not int
            or self.min_comparison_records < 1
        ):
            raise DatasetObservabilityError(
                "min_comparison_records must be a positive integer"
            )


@dataclass(frozen=True, slots=True, kw_only=True)
class MonitoringAlert:
    alert_id: str
    code: str
    severity: AlertSeverity
    metric: str
    observed: float
    threshold: float

    def __post_init__(self) -> None:
        for name in ("alert_id", "code", "metric"):
            _nonempty(name, getattr(self, name))
        if not isinstance(self.severity, AlertSeverity):
            raise DatasetObservabilityError("severity must be AlertSeverity")
        _unit("observed", self.observed)
        _unit("threshold", self.threshold)


@dataclass(frozen=True, slots=True, kw_only=True)
class MonitoringSnapshot:
    monitor_run_id: str
    dataset_id: str
    dataset_version: str
    baseline_dataset_id: str
    baseline_dataset_version: str
    baseline_quality_run_id: str
    comparison_quality_run_id: str
    recorded_at: datetime
    record_count: int
    baseline_pass_rate: float
    comparison_pass_rate: float
    pass_rate_drop: float
    drift_score: float
    status: MonitoringStatus
    policy: MonitoringPolicy
    alerts: tuple[MonitoringAlert, ...]

    def __post_init__(self) -> None:
        for name in (
            "monitor_run_id", "dataset_id", "dataset_version",
            "baseline_dataset_id", "baseline_dataset_version",
            "baseline_quality_run_id", "comparison_quality_run_id",
        ):
            _nonempty(name, getattr(self, name))
        if (
            not isinstance(self.recorded_at, datetime)
            or self.recorded_at.tzinfo is None
            or self.recorded_at.utcoffset() is None
        ):
            raise DatasetObservabilityError("recorded_at must be timezone-aware")
        if type(self.record_count) is not int or self.record_count < 1:
            raise DatasetObservabilityError("record_count must be positive")
        for name in (
            "baseline_pass_rate", "comparison_pass_rate",
            "pass_rate_drop", "drift_score",
        ):
            _unit(name, getattr(self, name))
        expected_drop = max(
            0.0, self.baseline_pass_rate - self.comparison_pass_rate
        )
        if abs(expected_drop - self.pass_rate_drop) > 1e-12:
            raise DatasetObservabilityError("pass_rate_drop is inconsistent")
        if not isinstance(self.status, MonitoringStatus):
            raise DatasetObservabilityError("status must be MonitoringStatus")
        if not isinstance(self.policy, MonitoringPolicy):
            raise DatasetObservabilityError("policy must be MonitoringPolicy")
        if not isinstance(self.alerts, tuple) or not all(
            isinstance(alert, MonitoringAlert) for alert in self.alerts
        ):
            raise DatasetObservabilityError("alerts must be a MonitoringAlert tuple")
        if len({alert.alert_id for alert in self.alerts}) != len(self.alerts):
            raise DatasetObservabilityError("duplicate alert identifiers")
        expected_status = (
            MonitoringStatus.CRITICAL
            if any(alert.severity is AlertSeverity.CRITICAL for alert in self.alerts)
            else MonitoringStatus.WARNING if self.alerts else MonitoringStatus.HEALTHY
        )
        if self.status is not expected_status:
            raise DatasetObservabilityError("status does not match alert severities")
