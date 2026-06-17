from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from src.evaluation.reporting.validators.dashboard_widget_validator import (
    DashboardWidgetValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class DashboardWidget:
    """
    Immutable dashboard widget.

    Represents a dashboard-ready widget payload
    for metrics, charts, tables, summaries,
    alerts, experiment trends, and benchmark
    analytics views.
    """

    widget_id: str

    title: str

    widget_type: str

    data: dict[
        str,
        Any,
    ]

    payload: dict[
        str,
        Any,
    ] | None = None

    order: int = 0

    width: int = 1

    height: int = 1

    description: str | None = None

    group: str | None = None

    refresh_interval_seconds: int | None = None

    metadata: dict[
        str,
        str,
    ] | None = None

    def __post_init__(
        self,
    ) -> None:
        DashboardWidgetValidator.validate(
            widget_id=self.widget_id,
            title=self.title,
            widget_type=self.widget_type,
            data=self.data,
            payload=self.payload,
            order=self.order,
            width=self.width,
            height=self.height,
            description=self.description,
            group=self.group,
            refresh_interval_seconds=(
                self.refresh_interval_seconds
            ),
            metadata=self.metadata,
        )

    @property
    def has_payload(
        self,
    ) -> bool:
        return bool(
            self.payload,
        )

    @property
    def has_description(
        self,
    ) -> bool:
        return (
            self.description
            is not None
        )

    @property
    def has_group(
        self,
    ) -> bool:
        return (
            self.group
            is not None
        )

    @property
    def has_metadata(
        self,
    ) -> bool:
        return bool(
            self.metadata,
        )

    @property
    def auto_refresh_enabled(
        self,
    ) -> bool:
        return (
            self.refresh_interval_seconds
            is not None
        )

    @property
    def is_metric(
        self,
    ) -> bool:
        return (
            self.widget_type
            == "metric"
        )

    @property
    def is_chart(
        self,
    ) -> bool:
        return (
            self.widget_type
            == "chart"
        )

    @property
    def is_table(
        self,
    ) -> bool:
        return (
            self.widget_type
            == "table"
        )

    @property
    def is_summary(
        self,
    ) -> bool:
        return (
            self.widget_type
            == "summary"
        )

    @property
    def is_alert(
        self,
    ) -> bool:
        return (
            self.widget_type
            == "alert"
        )

    @property
    def is_leaderboard(
        self,
    ) -> bool:
        return (
            self.widget_type
            == "leaderboard"
        )

    @property
    def is_heatmap(
        self,
    ) -> bool:
        return (
            self.widget_type
            == "heatmap"
        )

    @property
    def is_distribution(
        self,
    ) -> bool:
        return (
            self.widget_type
            == "distribution"
        )

    @property
    def area(
        self,
    ) -> int:
        return (
            self.width
            * self.height
        )

    @property
    def size(
        self,
    ) -> tuple[
        int,
        int,
    ]:
        return (
            self.width,
            self.height,
        )