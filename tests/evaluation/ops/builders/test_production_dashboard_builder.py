from __future__ import annotations

from datetime import datetime, timezone

from src.evaluation.ops.builders.production_evaluation_dashboard_builder import (
    ProductionEvaluationDashboardBuilder,
)
from src.evaluation.ops.enums.dashboard_severity import DashboardSeverity
from src.evaluation.ops.value_objects.dashboard_metric_card import DashboardMetricCard
from src.evaluation.ops.value_objects.dashboard_trend_point import DashboardTrendPoint


def test_production_dashboard_builder_should_sort_cards_and_trends() -> None:
    generated_at = datetime(2026, 1, 3, tzinfo=timezone.utc)
    older = datetime(2026, 1, 1, tzinfo=timezone.utc)
    newer = datetime(2026, 1, 2, tzinfo=timezone.utc)

    dashboard = ProductionEvaluationDashboardBuilder.build(
        dashboard_id="dashboard-1",
        title="Production Evaluation",
        generated_at=generated_at,
        metric_cards=(
            DashboardMetricCard(
                card_id="latency",
                title="Latency",
                value=120,
                formatted_value="120ms",
                severity=DashboardSeverity.WARNING,
                sort_order=2,
            ),
            DashboardMetricCard(
                card_id="score",
                title="Score",
                value=0.91,
                formatted_value="91%",
                severity=DashboardSeverity.SUCCESS,
                sort_order=1,
            ),
        ),
        trend_points=(
            DashboardTrendPoint(
                point_id="newer",
                metric_name="score",
                value=0.91,
                occurred_at=newer,
            ),
            DashboardTrendPoint(
                point_id="older",
                metric_name="score",
                value=0.88,
                occurred_at=older,
            ),
        ),
    )

    assert dashboard.dashboard_id == "dashboard-1"
    assert dashboard.generated_at == generated_at
    assert [card.card_id for card in dashboard.metric_cards] == ["score", "latency"]
    assert [point.point_id for point in dashboard.trend_points] == ["older", "newer"]
    assert dashboard.metric_by_id("score") is not None
    assert len(dashboard.trend_points_for_metric("score")) == 2
