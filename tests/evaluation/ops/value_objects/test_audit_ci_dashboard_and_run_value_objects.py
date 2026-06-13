from __future__ import annotations

from dataclasses import FrozenInstanceError
from datetime import datetime, timedelta, timezone

import pytest

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.ops.enums.audit_action import AuditAction
from src.evaluation.ops.enums.audit_aggregate_type import AuditAggregateType
from src.evaluation.ops.enums.audit_event_type import AuditEventType
from src.evaluation.ops.enums.audit_trigger import AuditTrigger
from src.evaluation.ops.enums.dashboard_severity import DashboardSeverity
from src.evaluation.ops.value_objects.audit_event import AuditEvent
from src.evaluation.ops.value_objects.ci_benchmark_policy_result import (
    CIBenchmarkPolicyResult,
)
from src.evaluation.ops.value_objects.dashboard_metric_card import DashboardMetricCard
from src.evaluation.ops.value_objects.dashboard_trend_point import DashboardTrendPoint
from src.evaluation.ops.value_objects.evaluation_run_result import EvaluationRunResult
from src.evaluation.ops.value_objects.quality_gate_result import QualityGateResult
from tests.evaluation.ops.factories import experiment_snapshot


def _gate(*, passed: bool, severity: str) -> QualityGateResult:
    return QualityGateResult(
        gate_name="minimum_overall_score",
        benchmark_id="benchmark-1",
        benchmark_name="AI Engineer Benchmark",
        benchmark_version="1.0.0",
        experiment_id="experiment-1",
        model_name="gpt-5",
        metric_name="overall_score",
        actual_value=0.90 if passed else 0.70,
        expected_value=0.80,
        overall_score=0.90 if passed else 0.70,
        minimum_required_score=0.80,
        passed=passed,
        severity=severity,
        interpretation="quality_gate_passed" if passed else "quality_gate_failed",
    )


def test_audit_event_should_freeze_metadata_and_expose_presence() -> None:
    event = AuditEvent(
        event_id="event-1",
        event_type=AuditEventType.EVALUATION_COMPLETED,
        aggregate_id="experiment-1",
        aggregate_type=AuditAggregateType.EXPERIMENT,
        benchmark_id="benchmark-1",
        experiment_id="experiment-1",
        model_name="gpt-5",
        occurred_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        actor="ci",
        action=AuditAction.EVALUATE,
        triggered_by=AuditTrigger.CI_PIPELINE,
        metadata={"overall_score": 0.91},
    )

    assert event.has_metadata is True
    assert event.metadata["overall_score"] == 0.91
    with pytest.raises(TypeError):
        event.metadata["new_key"] = "new_value"  # type: ignore[index]
    with pytest.raises(FrozenInstanceError):
        event.actor = "user"  # type: ignore[misc]


def test_ci_benchmark_policy_result_should_calculate_gate_helpers() -> None:
    passed_gate = _gate(passed=True, severity="info")
    failed_warning_gate = _gate(passed=False, severity="warning")

    result = CIBenchmarkPolicyResult(
        policy_name="release_policy",
        benchmark_id="benchmark-1",
        benchmark_name="AI Engineer Benchmark",
        benchmark_version="1.0.0",
        benchmark_score=0.90,
        minimum_required_score=0.80,
        experiment_id="experiment-1",
        overall_score=0.90,
        gate_results=(passed_gate, failed_warning_gate),
        blocking_failure_count=0,
        deployment_allowed=True,
        interpretation="ci_policy_passed",
    )

    assert result.total_gate_count == 2
    assert result.passed_gate_count == 1
    assert result.failed_gate_count == 1
    assert result.pass_rate == pytest.approx(0.5)
    assert result.has_blocking_failures is False


def test_dashboard_metric_card_should_expose_optional_field_helpers() -> None:
    card = DashboardMetricCard(
        card_id="score",
        title="Score",
        value=0.91,
        formatted_value="91%",
        description="Overall quality score",
        trend_value=0.03,
        trend_label="+3%",
        is_positive_trend=True,
        severity=DashboardSeverity.SUCCESS,
        sort_order=1,
    )

    assert card.has_trend is True
    assert card.has_description is True
    assert card.has_severity is True


def test_dashboard_trend_point_should_expose_display_and_presence_helpers() -> None:
    point = DashboardTrendPoint(
        point_id="point-1",
        metric_name="latency",
        value=120,
        occurred_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        unit="ms",
        benchmark_id="benchmark-1",
        experiment_id="experiment-1",
        model_name="gpt-5",
        label="p95",
    )

    assert point.has_unit is True
    assert point.has_benchmark is True
    assert point.has_experiment is True
    assert point.has_model is True
    assert point.has_label is True
    assert point.display_value == "120ms"


def test_evaluation_run_result_should_proxy_snapshot_and_ci_helpers() -> None:
    snapshot = experiment_snapshot(overall_score=0.91)
    started_at = datetime(2026, 1, 1, tzinfo=timezone.utc)
    completed_at = started_at + timedelta(seconds=5)
    gate = _gate(passed=True, severity="info")
    ci_result = CIBenchmarkPolicyResult(
        policy_name="release_policy",
        benchmark_id=snapshot.benchmark_id,
        benchmark_name=snapshot.benchmark_name,
        benchmark_version=snapshot.benchmark_version,
        benchmark_score=0.91,
        minimum_required_score=0.80,
        experiment_id=snapshot.experiment_id,
        overall_score=0.91,
        gate_results=(gate,),
        blocking_failure_count=0,
        deployment_allowed=True,
        interpretation="ci_policy_passed",
    )

    result = EvaluationRunResult(
        run_id="run-1",
        experiment_snapshot=snapshot,
        started_at=started_at,
        completed_at=completed_at,
        duration_seconds=5.0,
        success=True,
        quality_gate_result=gate,
        ci_policy_result=ci_result,
    )

    assert result.experiment_id == snapshot.experiment_id
    assert result.benchmark_id == snapshot.benchmark_id
    assert result.model_name == snapshot.model_name
    assert result.overall_score == snapshot.overall_score
    assert result.ci_passed is True
    assert result.has_ci_policy is True
    assert result.deployment_allowed is True
    assert result.has_blocking_failures is False
    assert result.blocking_failure_count == 0
    assert result.ci_interpretation == "ci_policy_passed"


def test_evaluation_run_result_should_require_error_message_for_failed_runs() -> None:
    snapshot = experiment_snapshot()
    started_at = datetime(2026, 1, 1, tzinfo=timezone.utc)

    with pytest.raises(EvaluationValidationError, match="error_message"):
        EvaluationRunResult(
            run_id="run-1",
            experiment_snapshot=snapshot,
            started_at=started_at,
            completed_at=started_at + timedelta(seconds=1),
            duration_seconds=1.0,
            success=False,
        )
