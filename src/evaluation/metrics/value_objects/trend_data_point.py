from __future__ import annotations

from dataclasses import dataclass

from src.evaluation.metrics.validators.trend_data_point_validator import (
    TrendDataPointValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class TrendDataPoint:
    """
    Immutable trend data point.
    """

    label: str
    value: float

    def __post_init__(
        self,
    ) -> None:
        TrendDataPointValidator.validate(
            label=self.label,
            value=self.value,
        )