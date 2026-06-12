from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from src.evaluation.ops.builders.dashboard_metric_card_collection_builder import (
    DashboardMetricCardCollectionBuilder,
)
from src.evaluation.ops.builders.dashboard_trend_collection_builder import (
    DashboardTrendCollectionBuilder,
)
from src.evaluation.ops.entities.dashboard_metric_card import (
    DashboardMetricCard,
)
from src.evaluation.ops.entities.production_evaluation_dashboard import (
    ProductionEvaluationDashboard,
)
from src.evaluation.ops.value_objects.dashboard_trend_point import (
    DashboardTrendPoint,
)


class ProductionEvaluationDashboardBuilder:
    """
    Builds production evaluation dashboards.
    """

    @staticmethod
    def build(
        *,
        title: str,
        metric_cards: tuple[
            DashboardMetricCard,
            ...,
        ],
        trend_points: tuple[
            DashboardTrendPoint,
            ...,
        ] = (),
        dashboard_id: str | None = None,
        generated_at: datetime | None = None,
        notes: str | None = None,
    ) -> ProductionEvaluationDashboard:
        return ProductionEvaluationDashboard(
            dashboard_id=(
                dashboard_id
                or str(uuid4())
            ),
            title=title,
            generated_at=(
                generated_at
                or datetime.now(UTC)
            ),
            metric_cards=(
                DashboardMetricCardCollectionBuilder.build(
                    metric_cards=metric_cards,
                )
            ),
            trend_points=(
                DashboardTrendCollectionBuilder.build(
                    trend_points=trend_points,
                )
            ),
            notes=notes,
        )