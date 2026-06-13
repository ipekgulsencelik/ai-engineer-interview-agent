from __future__ import annotations

from datetime import datetime, timezone

from src.evaluation.ops.entities.evaluation_audit_trail import EvaluationAuditTrail
from src.evaluation.ops.entities.production_evaluation_dashboard import (
    ProductionEvaluationDashboard,
)
from src.evaluation.ops.enums.audit_action import AuditAction
from src.evaluation.ops.enums.audit_aggregate_type import AuditAggregateType
from src.evaluation.ops.enums.audit_event_type import AuditEventType
from src.evaluation.ops.enums.audit_trigger import AuditTrigger
from src.evaluation.ops.value_objects.audit_event import AuditEvent
from src.evaluation.ops.value_objects.dashboard_metric_card import DashboardMetricCard
from src.evaluation.ops.value_objects.dashboard_trend_point import DashboardTrendPoint


def _event(
    *,
    event_id: str,
    event_type: AuditEventType,
    aggregate_id: str,
    occurred_at: datetime,
) -> AuditEvent:
    return AuditEvent(
        event_id=event_id,
        event_type=event_type,
        aggregate_id=aggregate_id,
        aggregate_type=AuditAggregateType.EXPERIMENT,
        benchmark_id="benchmark-1",
        experiment_id="experiment-1",
        model_name="gpt-5",
        occurred_at=occurred_at,
        actor="ci",
        action=AuditAction.EVALUATE,
        triggered_by=AuditTrigger.CI_PIPELINE,
        metadata={"event_id": event_id},
    )


def test_evaluation_audit_trail_should_expose_event_helpers() -> None:
    first_time = datetime(2026, 1, 1, tzinfo=timezone.utc)
    second_time = datetime(2026, 1, 2, tzinfo=timezone.utc)
    first_event = _event(
        event_id="event-1",
        event_type=AuditEventType.EVALUATION_STARTED,
        aggregate_id="experiment-1",
        occurred_at=first_time,
    )
    second_event = _event(
        event_id="event-2",
        event_type=AuditEventType.EVALUATION_COMPLETED,
        aggregate_id="experiment-2",
        occurred_at=second_time,
    )

    trail = EvaluationAuditTrail(
        trail_id="trail-1",
        evaluation_run_id="run-1",
        experiment_id="experiment-1",
        benchmark_id="benchmark-1",
        events=(first_event, second_event),
        created_at=first_time,
    )

    assert trail.event_count == 2
    assert trail.has_events is True
    assert trail.first_event == first_event
    assert trail.last_event == second_event
    assert trail.started_at == first_time
    assert trail.latest_occurred_at == second_time
    assert trail.contains_event_type(AuditEventType.EVALUATION_COMPLETED) is True
    assert trail.events_for_aggregate("experiment-2") == (second_event,)


def test_production_evaluation_dashboard_should_expose_metric_and_trend_helpers() -> (
    None
):
    generated_at = datetime(2026, 1, 1, tzinfo=timezone.utc)
    score_card = DashboardMetricCard(
        card_id="score",
        title="Score",
        value=0.91,
        formatted_value="91%",
    )
    trend_point = DashboardTrendPoint(
        point_id="point-1",
        metric_name="score",
        value=0.91,
        occurred_at=generated_at,
    )

    dashboard = ProductionEvaluationDashboard(
        dashboard_id="dashboard-1",
        title="Production Evaluation",
        generated_at=generated_at,
        metric_cards=(score_card,),
        trend_points=(trend_point,),
    )

    assert dashboard.metric_count == 1
    assert dashboard.trend_point_count == 1
    assert dashboard.has_metrics is True
    assert dashboard.has_trends is True
    assert dashboard.metric_by_id("score") == score_card
    assert dashboard.metric_by_id("missing") is None
    assert dashboard.trend_points_for_metric("score") == (trend_point,)
    assert dashboard.trend_points_for_metric("missing") == ()
