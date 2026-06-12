from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from src.evaluation.ops.validators.dashboard_trend_point_validator import (
    DashboardTrendPointValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class DashboardTrendPoint:
    """
    Immutable dashboard trend point.

    Represents a single time-series point used in
    evaluation dashboard trend charts.
    """

    point_id: str

    metric_name: str

    value: float

    occurred_at: datetime

    unit: str | None = None

    benchmark_id: str | None = None

    experiment_id: str | None = None

    model_name: str | None = None

    label: str | None = None

    notes: str | None = None

    def __post_init__(
        self,
    ) -> None:
        DashboardTrendPointValidator.validate(
            point_id=self.point_id,
            metric_name=self.metric_name,
            value=self.value,
            occurred_at=self.occurred_at,
            unit=self.unit,
            benchmark_id=self.benchmark_id,
            experiment_id=self.experiment_id,
            model_name=self.model_name,
            label=self.label,
            notes=self.notes,
        )

    @property
    def has_unit(
        self,
    ) -> bool:
        return self.unit is not None

    @property
    def has_benchmark(
        self,
    ) -> bool:
        return self.benchmark_id is not None

    @property
    def has_experiment(
        self,
    ) -> bool:
        return self.experiment_id is not None

    @property
    def has_model(
        self,
    ) -> bool:
        return self.model_name is not None

    @property
    def has_label(
        self,
    ) -> bool:
        return self.label is not None

    @property
    def display_value(
        self,
    ) -> str:
        if self.unit is None:
            return str(self.value)
        return f"{self.value}{self.unit}"