from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from src.evaluation.ops.entities.dashboard_metric_card import (
    DashboardMetricCard,
)
from src.evaluation.ops.value_objects.dashboard_trend_point import (
    DashboardTrendPoint,
)
from src.evaluation.ops.validators.production_evaluation_dashboard_validator import (
    ProductionEvaluationDashboardValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ProductionEvaluationDashboard:
    """
    Immutable production evaluation dashboard.

    Represents the complete dashboard state used
    for benchmark monitoring, quality tracking,
    regression visibility, and operational reporting.
    """

    dashboard_id: str

    title: str

    generated_at: datetime

    metric_cards: tuple[
        DashboardMetricCard,
        ...,
    ]

    trend_points: tuple[
        DashboardTrendPoint,
        ...,
    ]

    notes: str | None = None

    def __post_init__(
        self,
    ) -> None:
        ProductionEvaluationDashboardValidator.validate(
            dashboard_id=self.dashboard_id,
            title=self.title,
            generated_at=self.generated_at,
            metric_cards=self.metric_cards,
            trend_points=self.trend_points,
            notes=self.notes,
        )

    @property
    def metric_count(
        self,
    ) -> int:
        return len(
            self.metric_cards,
        )

    @property
    def trend_point_count(
        self,
    ) -> int:
        return len(
            self.trend_points,
        )

    @property
    def has_metrics(
        self,
    ) -> bool:
        return bool(
            self.metric_cards,
        )

    @property
    def has_trends(
        self,
    ) -> bool:
        return bool(
            self.trend_points,
        )

    def metric_by_id(
        self,
        card_id: str,
    ) -> DashboardMetricCard | None:
        return next(
            (
                card
                for card in self.metric_cards
                if card.card_id == card_id
            ),
            None,
        )

    def trend_points_for_metric(
        self,
        metric_name: str,
    ) -> tuple[
        DashboardTrendPoint,
        ...,
    ]:
        return tuple(
            point
            for point in self.trend_points
            if point.metric_name
            == metric_name
        )