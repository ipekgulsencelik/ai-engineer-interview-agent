from __future__ import annotations

from dataclasses import dataclass

from src.evaluation.metrics.validators.trend_visualization_snapshot_validator import (
    TrendVisualizationSnapshotValidator,
)
from src.evaluation.metrics.value_objects.trend_data_point import (
    TrendDataPoint,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class TrendVisualizationSnapshot:
    """
    Immutable trend visualization snapshot.

    Represents chart-ready benchmark trend data.
    """

    title: str
    description: str

    trend_direction: str

    data_points: tuple[
        TrendDataPoint,
        ...,
    ]

    notes: str | None = None

    def __post_init__(
        self,
    ) -> None:
        TrendVisualizationSnapshotValidator.validate(
            title=self.title,
            description=self.description,
            trend_direction=self.trend_direction,
            data_points=self.data_points,
            notes=self.notes,
        )

    @property
    def point_count(
        self,
    ) -> int:
        return len(
            self.data_points,
        )

    @property
    def first_value(
        self,
    ) -> float:
        return (
            self.data_points[0]
            .value
        )

    @property
    def last_value(
        self,
    ) -> float:
        return (
            self.data_points[-1]
            .value
        )

    @property
    def delta(
        self,
    ) -> float:
        return (
            self.last_value
            - self.first_value
        )

    @property
    def has_positive_trend(
        self,
    ) -> bool:
        return self.delta > 0

    @property
    def has_negative_trend(
        self,
    ) -> bool:
        return self.delta < 0

    @property
    def is_flat_trend(
        self,
    ) -> bool:
        return self.delta == 0