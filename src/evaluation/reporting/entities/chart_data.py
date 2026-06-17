from __future__ import annotations

from dataclasses import dataclass

from src.evaluation.reporting.validators.chart_data_validator import (
    ChartDataValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ChartData:
    """
    Immutable chart data value object.

    Represents chart-ready data for dashboards,
    reports, visual analytics, trend analysis,
    benchmark summaries, and experiment tracking.
    """

    title: str

    chart_type: str

    labels: tuple[
        str,
        ...,
    ]

    scores: tuple[
        float,
        ...,
    ]

    average_score: float | None = None

    trend_direction: str | None = None

    x_axis_label: str | None = None

    y_axis_label: str | None = None

    series_name: str | None = None

    metric_name: str | None = None

    description: str | None = None

    metadata: dict[
        str,
        str,
    ] | None = None

    def __post_init__(
        self,
    ) -> None:
        ChartDataValidator.validate(
            title=self.title,
            chart_type=self.chart_type,
            labels=self.labels,
            scores=self.scores,
            average_score=self.average_score,
            trend_direction=self.trend_direction,
            x_axis_label=self.x_axis_label,
            y_axis_label=self.y_axis_label,
            series_name=self.series_name,
            metric_name=self.metric_name,
            description=self.description,
            metadata=self.metadata,
        )

    @property
    def point_count(
        self,
    ) -> int:
        return len(
            self.scores,
        )

    @property
    def max_score(
        self,
    ) -> float | None:
        if not self.scores:
            return None

        return max(
            self.scores,
        )

    @property
    def min_score(
        self,
    ) -> float | None:
        if not self.scores:
            return None

        return min(
            self.scores,
        )

    @property
    def latest_score(
        self,
    ) -> float | None:
        if not self.scores:
            return None

        return self.scores[
            -1
        ]

    @property
    def has_average_score(
        self,
    ) -> bool:
        return (
            self.average_score
            is not None
        )

    @property
    def has_trend_direction(
        self,
    ) -> bool:
        return (
            self.trend_direction
            is not None
        )

    @property
    def has_metric_name(
        self,
    ) -> bool:
        return (
            self.metric_name
            is not None
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
    def has_metadata(
        self,
    ) -> bool:
        return bool(
            self.metadata,
        )

    @property
    def is_line_chart(
        self,
    ) -> bool:
        return (
            self.chart_type == "line"
        )

    @property
    def is_bar_chart(
        self,
    ) -> bool:
        return (
            self.chart_type == "bar"
        )

    @property
    def is_pie_chart(
        self,
    ) -> bool:
        return (
            self.chart_type == "pie"
        )

    @property
    def is_scatter_chart(
        self,
    ) -> bool:
        return (
            self.chart_type == "scatter"
        )