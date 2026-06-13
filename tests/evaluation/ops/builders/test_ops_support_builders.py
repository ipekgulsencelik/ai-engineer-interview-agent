from __future__ import annotations

from datetime import datetime, timezone

from src.evaluation.ops.builders.ci_benchmark_policy_result_builder import (
    CIBenchmarkPolicyResultBuilder,
)
from src.evaluation.ops.builders.dashboard_metric_card_collection_builder import (
    DashboardMetricCardCollectionBuilder,
)
from src.evaluation.ops.builders.dashboard_trend_collection_builder import (
    DashboardTrendCollectionBuilder,
)
from src.evaluation.ops.builders.evaluation_audit_trail_builder import (
    EvaluationAuditTrailBuilder,
)
from src.evaluation.ops.builders.evaluation_run_result_builder import (
    EvaluationRunResultBuilder,
)
from src.evaluation.ops.builders.quality_gate_result_builder import (
    QualityGateResultBuilder,
)
from src.evaluation.ops.enums.audit_action import AuditAction
from src.evaluation.ops.enums.audit_aggregate_type import AuditAggregateType
from src.evaluation.ops.enums.audit_event_type import AuditEventType
from src.evaluation.ops.enums.audit_trigger import AuditTrigger
from src.evaluation.ops.enums.dashboard_severity import DashboardSeverity
from src.evaluation.ops.value_objects.audit_event import AuditEvent
from src.evaluation.ops.value_objects.dashboard_metric_card import DashboardMetricCard
from src.evaluation.ops.value_objects.dashboard_trend_point import DashboardTrendPoint
from src.evaluation.ops.value_objects.quality_gate_result import QualityGateResult
from tests.evaluation.ops.factories import experiment_snapshot


def _audit_event(*, occurred_at: datetime) -> AuditEvent:
    return AuditEvent(
        event_id="event-1",
        event_type=AuditEventType.EVALUATION_STARTED,
        aggregate_id="experiment-1",
        aggregate_type=AuditAggregateType.EXPERIMENT,
        benchmark_id="benchmark-1",
        experiment_id="experiment-1",
        model_name="gpt-5",
        occurred_at=occurred_at,
        actor="ci",
        action=AuditAction.CREATE,
        triggered_by=AuditTrigger.CI_PIPELINE,
        metadata={"stage": "start"},
    )


def test_ci_benchmark_policy_result_builder_should_copy_snapshot_metadata() -> None:
    snapshot = experiment_snapshot(overall_score=0.91)
    gate = QualityGateResult(
        gate_name="minimum_overall_score",
        benchmark_id=snapshot.benchmark_id,
        benchmark_name=snapshot.benchmark_name,
        benchmark_version=snapshot.benchmark_version,
        experiment_id=snapshot.experiment_id,
        model_name=snapshot.model_name,
        metric_name="overall_score",
        actual_value=0.91,
        expected_value=0.80,
        overall_score=0.91,
        minimum_required_score=0.80,
        passed=True,
        severity="info",
        interpretation="quality_gate_passed",
    )

    result = CIBenchmarkPolicyResultBuilder.build(
        policy_name="release_policy",
        snapshot=snapshot,
        minimum_required_score=0.80,
        gate_results=(gate,),
        blocking_failure_count=0,
        deployment_allowed=True,
        notes="ready",
    )

    assert result.policy_name == "release_policy"
    assert result.benchmark_id == snapshot.benchmark_id
    assert result.benchmark_score == snapshot.overall_score
    assert result.gate_results == (gate,)
    assert result.interpretation == "ci_policy_passed"
    assert result.notes == "ready"


def test_quality_gate_result_builder_should_resolve_passed_and_failed_severity() -> (
    None
):
    snapshot = experiment_snapshot(overall_score=0.78)

    failed_gate = QualityGateResultBuilder.build(
        gate_name="minimum_overall_score",
        snapshot=snapshot,
        metric_name="overall_score",
        actual_value=0.78,
        expected_value=0.80,
        minimum_required_score=0.80,
        passed=False,
    )
    passed_gate = QualityGateResultBuilder.build(
        gate_name="minimum_overall_score",
        snapshot=snapshot,
        metric_name="overall_score",
        actual_value=0.82,
        expected_value=0.80,
        minimum_required_score=0.80,
        passed=True,
    )

    assert failed_gate.severity == "critical"
    assert failed_gate.interpretation == "quality_gate_failed"
    assert failed_gate.overall_score == snapshot.overall_score
    assert passed_gate.severity == "info"
    assert passed_gate.interpretation == "quality_gate_passed"


def test_collection_builders_should_sort_dashboard_cards_and_trend_points() -> None:
    first_time = datetime(2026, 1, 1, tzinfo=timezone.utc)
    second_time = datetime(2026, 1, 2, tzinfo=timezone.utc)
    cards = (
        DashboardMetricCard(
            card_id="second",
            title="Second",
            value=2,
            formatted_value="2",
            severity=DashboardSeverity.INFO,
            sort_order=2,
        ),
        DashboardMetricCard(
            card_id="first",
            title="First",
            value=1,
            formatted_value="1",
            severity=DashboardSeverity.SUCCESS,
            sort_order=1,
        ),
    )
    trend_points = (
        DashboardTrendPoint(
            point_id="second",
            metric_name="score",
            value=0.9,
            occurred_at=second_time,
        ),
        DashboardTrendPoint(
            point_id="first",
            metric_name="score",
            value=0.8,
            occurred_at=first_time,
        ),
    )

    sorted_cards = DashboardMetricCardCollectionBuilder.build(metric_cards=cards)
    sorted_trends = DashboardTrendCollectionBuilder.build(trend_points=trend_points)

    assert [card.card_id for card in sorted_cards] == ["first", "second"]
    assert [point.point_id for point in sorted_trends] == ["first", "second"]


def test_evaluation_audit_trail_builder_should_create_trail_from_snapshot() -> None:
    created_at = datetime(2026, 1, 3, tzinfo=timezone.utc)
    snapshot = experiment_snapshot()
    event = _audit_event(occurred_at=created_at)

    trail = EvaluationAuditTrailBuilder.build(
        evaluation_run_id="run-1",
        snapshot=snapshot,
        events=(event,),
        created_at=created_at,
    )

    assert trail.evaluation_run_id == "run-1"
    assert trail.experiment_id == snapshot.experiment_id
    assert trail.benchmark_id == snapshot.benchmark_id
    assert trail.events == (event,)
    assert trail.created_at == created_at


def test_evaluation_run_result_builder_should_attach_ci_gate_and_failure_message() -> (
    None
):
    snapshot = experiment_snapshot(overall_score=0.70)
    started_at = datetime(2026, 1, 1, tzinfo=timezone.utc)
    completed_at = datetime(2026, 1, 1, 0, 0, 5, tzinfo=timezone.utc)
    failed_gate = QualityGateResult(
        gate_name="minimum_overall_score",
        benchmark_id=snapshot.benchmark_id,
        benchmark_name=snapshot.benchmark_name,
        benchmark_version=snapshot.benchmark_version,
        experiment_id=snapshot.experiment_id,
        model_name=snapshot.model_name,
        metric_name="overall_score",
        actual_value=0.70,
        expected_value=0.80,
        overall_score=0.70,
        minimum_required_score=0.80,
        passed=False,
        severity="critical",
        interpretation="quality_gate_failed",
    )
    ci_policy_result = CIBenchmarkPolicyResultBuilder.build(
        policy_name="release_policy",
        snapshot=snapshot,
        minimum_required_score=0.80,
        gate_results=(failed_gate,),
        blocking_failure_count=1,
        deployment_allowed=False,
    )

    result = EvaluationRunResultBuilder.build(
        run_id="run-1",
        snapshot=snapshot,
        started_at=started_at,
        completed_at=completed_at,
        duration_seconds=5.0,
        success=False,
        ci_policy_result=ci_policy_result,
    )

    assert result.quality_gate_result == failed_gate
    assert result.ci_policy_result == ci_policy_result
    assert result.error_message == "ci_policy_failed"
