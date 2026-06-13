from __future__ import annotations

from datetime import UTC, datetime

from src.evaluation.ops.builders.dashboard_metric_cards_composer import (
    DashboardMetricCardsComposer,
)
from src.evaluation.ops.builders.dashboard_trend_points_builder import (
    DashboardTrendPointsBuilder,
)
from src.evaluation.ops.entities.production_evaluation_dashboard import (
    ProductionEvaluationDashboard,
)


class EvaluationDashboardModelBuilder:
    """
    Builds production evaluation dashboard read models.
    """

    def __init__(
        self,
        *,
        metric_cards_composer: DashboardMetricCardsComposer | None = None,
        trend_points_builder: DashboardTrendPointsBuilder | None = None,
    ) -> None:
        self._metric_cards_composer = (
            metric_cards_composer
            or DashboardMetricCardsComposer()
        )
        self._trend_points_builder = (
            trend_points_builder
            or DashboardTrendPointsBuilder()
        )

    def build(
        self,
        *,
        dashboard_id: str,
        aggregate_result,
        trend_snapshot,
        leaderboard_entries,
        regression_result,
        ci_policy_result,
        generated_at: datetime | None = None,
        notes: str | None = None,
    ) -> ProductionEvaluationDashboard:
        return ProductionEvaluationDashboard(
            dashboard_id=dashboard_id,
            title=aggregate_result.benchmark_name,
            generated_at=(
                generated_at
                or datetime.now(UTC)
            ),
            metric_cards=(
                self._metric_cards_composer.compose(
                    aggregate_result=aggregate_result,
                    regression_result=regression_result,
                    ci_policy_result=ci_policy_result,
                    leaderboard_entries=leaderboard_entries,
                )
            ),
            trend_points=(
                self._trend_points_builder.build(
                    trend_snapshot=trend_snapshot,
                )
            ),
            notes=notes,
        )