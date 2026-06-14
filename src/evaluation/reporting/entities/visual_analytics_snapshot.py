from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from src.evaluation.reporting.enums.summary_trend_direction import (
    SummaryTrendDirection,
)
from src.evaluation.reporting.validators.visual_analytics_snapshot_validator import (
    VisualAnalyticsSnapshotValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class VisualAnalyticsSnapshot:
    """
    Immutable visual analytics snapshot.

    Represents chart-ready analytics data generated
    from experiment runs, comparisons, trends,
    dashboards, or benchmark reports.
    """

    snapshot_id: str

    title: str

    chart_type: str

    created_at: datetime

    labels: tuple[
        str,
        ...,
    ]

    scores: tuple[
        float,
        ...,
    ]

    average_score: float | None = None

    trend_direction: SummaryTrendDirection | None = None

    x_axis_label: str | None = None

    y_axis_label: str | None = None

    series_name: str | None = None

    experiment_id: str | None = None

    run_id: str | None = None

    benchmark_id: str | None = None

    model_name: str | None = None

    description: str | None = None

    metadata: dict[
        str,
        str,
    ] | None = None

    def __post_init__(
        self,
    ) -> None:
        VisualAnalyticsSnapshotValidator.validate(
            snapshot_id=self.snapshot_id,
            title=self.title,
            chart_type=self.chart_type,
            created_at=self.created_at,
            labels=self.labels,
            scores=self.scores,
            average_score=self.average_score,
            trend_direction=self.trend_direction,
            x_axis_label=self.x_axis_label,
            y_axis_label=self.y_axis_label,
            series_name=self.series_name,
            experiment_id=self.experiment_id,
            run_id=self.run_id,
            benchmark_id=self.benchmark_id,
            model_name=self.model_name,
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
    def has_labels(
        self,
    ) -> bool:
        return bool(
            self.labels,
        )

    @property
    def has_scores(
        self,
    ) -> bool:
        return bool(
            self.scores,
        )

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
    def is_improving(
        self,
    ) -> bool:
        return (
            self.trend_direction
            == SummaryTrendDirection.IMPROVING
        )

    @property
    def is_declining(
        self,
    ) -> bool:
        return (
            self.trend_direction
            == SummaryTrendDirection.DECLINING
        )

    @property
    def is_stable(
        self,
    ) -> bool:
        return (
            self.trend_direction
            == SummaryTrendDirection.STABLE
        )

    @property
    def is_volatile(
        self,
    ) -> bool:
        return (
            self.trend_direction
            == SummaryTrendDirection.VOLATILE
        )

    @property
    def has_metadata(
        self,
    ) -> bool:
        return bool(
            self.metadata,
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
    def has_context(
        self,
    ) -> bool:
        return (
            self.experiment_id is not None
            or self.run_id is not None
            or self.benchmark_id is not None
            or self.model_name is not None
        )