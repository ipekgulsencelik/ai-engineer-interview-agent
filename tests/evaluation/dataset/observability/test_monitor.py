"""Behavioral tests for rule-based quality monitoring and drift alerts."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from src.evaluation.dataset.observability import (
    AlertSeverity,
    DatasetObservabilityError,
    DatasetObservabilityMonitor,
    MonitoringPolicy,
    MonitoringSnapshotSerializer,
    MonitoringStatus,
)
from src.evaluation.dataset.quality.models import (
    IssueSeverity,
    QualityIssue,
    QualityReport,
)
from src.evaluation.dataset.value_objects.dataset_distribution_snapshot import (
    DatasetDistributionSnapshot,
)


def distribution(
    *,
    name: str = "dataset",
    category_a: int = 10,
    category_b: int = 0,
) -> DatasetDistributionSnapshot:
    return DatasetDistributionSnapshot(
        dataset_id=name,
        sample_count=category_a + category_b,
        category_distribution={"RAG": category_a, "Agents": category_b},
        level_distribution={"MID": category_a + category_b},
        split_distribution={"UNSPLIT": category_a + category_b},
    )


def quality(
    *,
    name: str = "dataset",
    run_id: str = "quality-run",
    passed: int = 10,
    accepted: bool = True,
    checked_at: datetime | None = None,
) -> QualityReport:
    issues = tuple(
        QualityIssue(
            rule_id="test-rule",
            code="warning",
            message="A check failed without exposing sample contents.",
            severity=IssueSeverity.WARNING,
            record_index=index,
        )
        for index in range(10 - passed)
    )
    return QualityReport(
        run_id=run_id,
        dataset_id=name,
        dataset_version="1.0.0",
        checked_at=checked_at or datetime(2026, 11, 10, tzinfo=UTC),
        record_count=10,
        total_checks=10,
        passed_checks=passed,
        failed_checks=10 - passed,
        error_count=0,
        warning_count=len(issues),
        failed_record_count=len(issues),
        pass_rate=passed / 10,
        accepted=accepted,
        issues=issues,
    )


class FixedClock:
    def now(self) -> datetime:
        return datetime(2026, 11, 10, 12, tzinfo=UTC)


def monitor(policy: MonitoringPolicy | None = None) -> DatasetObservabilityMonitor:
    return DatasetObservabilityMonitor(
        policy=policy,
        clock=FixedClock(),
        id_factory=lambda: "monitor-1",
    )


def evaluate(
    *,
    baseline: DatasetDistributionSnapshot | None = None,
    comparison: DatasetDistributionSnapshot | None = None,
    baseline_quality: QualityReport | None = None,
    comparison_quality: QualityReport | None = None,
    policy: MonitoringPolicy | None = None,
):
    return monitor(policy).evaluate(
        baseline_distribution=baseline if baseline is not None else distribution(),
        comparison_distribution=(
            comparison if comparison is not None else distribution()
        ),
        baseline_quality=(
            baseline_quality if baseline_quality is not None
            else quality(run_id="baseline")
        ),
        comparison_quality=(
            comparison_quality if comparison_quality is not None
            else quality(run_id="comparison")
        ),
    )


def test_healthy_monitoring_has_no_alerts_and_serializes_roundtrip() -> None:
    snapshot = evaluate()
    assert snapshot.status is MonitoringStatus.HEALTHY
    assert snapshot.alerts == ()
    assert snapshot.pass_rate_drop == 0.0
    assert snapshot.drift_score == 0.0
    payload = MonitoringSnapshotSerializer.serialize(snapshot)
    assert MonitoringSnapshotSerializer.deserialize(payload) == snapshot


def test_warning_drift_reuses_existing_distribution_drift_analyzer() -> None:
    snapshot = evaluate(comparison=distribution(category_a=8, category_b=2))
    assert snapshot.status is MonitoringStatus.WARNING
    assert snapshot.drift_score == pytest.approx(0.2)
    assert len(snapshot.alerts) == 1
    alert = snapshot.alerts[0]
    assert alert.code == "DRIFT_WARNING"
    assert alert.metric == "distribution_drift"
    assert alert.severity is AlertSeverity.WARNING
    assert alert.alert_id == "monitor-1:DRIFT_WARNING"


def test_critical_drift_and_rejected_quality_gate_are_distinct_alerts() -> None:
    snapshot = evaluate(
        comparison=distribution(category_a=5, category_b=5),
        comparison_quality=quality(run_id="comparison", accepted=False),
    )
    assert snapshot.status is MonitoringStatus.CRITICAL
    assert {alert.code for alert in snapshot.alerts} == {
        "DRIFT_CRITICAL", "QUALITY_GATE_REJECTED",
    }


@pytest.mark.parametrize(
    "passed,expected",
    [
        (10, None),
        (9, "QUALITY_REGRESSION_WARNING"),
        (7, "QUALITY_REGRESSION_CRITICAL"),
    ],
)
def test_quality_regression_thresholds(
    passed: int, expected: str | None
) -> None:
    snapshot = evaluate(
        comparison_quality=quality(run_id="comparison", passed=passed)
    )
    codes = {alert.code for alert in snapshot.alerts}
    if expected is None:
        assert not codes
    else:
        assert expected in codes
    assert snapshot.pass_rate_drop == pytest.approx((10 - passed) / 10)


def test_small_sample_size_emits_critical_alert() -> None:
    snapshot = evaluate(
        policy=MonitoringPolicy(min_comparison_records=11)
    )
    assert snapshot.status is MonitoringStatus.CRITICAL
    assert {alert.code for alert in snapshot.alerts} == {
        "INSUFFICIENT_SAMPLES",
    }


@pytest.mark.parametrize(
    "kwargs",
    [
        {"drift_warning": float("nan")},
        {"drift_warning": -0.1},
        {"drift_warning": 0.4, "drift_critical": 0.1},
        {"pass_rate_drop_warning": 0.5, "pass_rate_drop_critical": 0.1},
        {"min_comparison_records": True},
        {"min_comparison_records": 0},
    ],
)
def test_policy_rejects_invalid_limits(kwargs: dict) -> None:
    with pytest.raises(DatasetObservabilityError):
        MonitoringPolicy(**kwargs)


def test_monitor_rejects_mismatched_distribution_and_quality_identity() -> None:
    with pytest.raises(DatasetObservabilityError, match="dataset differ"):
        evaluate(
            comparison=distribution(name="other"),
        )


def test_monitor_rejects_inconsistent_distribution_counts() -> None:
    malformed = distribution()
    malformed.category_distribution["RAG"] = 9
    with pytest.raises(DatasetObservabilityError, match="counts do not match"):
        evaluate(comparison=malformed)


def test_monitor_rejects_empty_distributions_to_avoid_false_zero_drift() -> None:
    empty = DatasetDistributionSnapshot(
        dataset_id="dataset",
        sample_count=0,
        category_distribution={"RAG": 0},
        level_distribution={"MID": 0},
        split_distribution={"UNSPLIT": 0},
    )
    with pytest.raises(DatasetObservabilityError, match="nonempty"):
        evaluate(comparison=empty)


def test_monitor_rejects_equal_quality_run_ids() -> None:
    with pytest.raises(DatasetObservabilityError, match="must differ"):
        evaluate(comparison_quality=quality(run_id="baseline"))


def test_monitor_rejects_newer_baseline_report() -> None:
    latest = datetime(2026, 11, 11, tzinfo=UTC)
    previous = latest - timedelta(days=1)
    with pytest.raises(DatasetObservabilityError, match="not be newer"):
        evaluate(
            baseline_quality=quality(run_id="baseline", checked_at=latest),
            comparison_quality=quality(run_id="comparison", checked_at=previous),
        )


def test_monitor_rejects_quality_and_distribution_record_count_mismatch() -> None:
    with pytest.raises(DatasetObservabilityError, match="counts differ"):
        evaluate(comparison=distribution(category_a=9, category_b=0))
