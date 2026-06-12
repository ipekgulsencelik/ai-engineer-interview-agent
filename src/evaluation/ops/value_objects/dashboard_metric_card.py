from __future__ import annotations

from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class DashboardMetricCard:
    """
    Immutable dashboard metric card.

    Represents a single dashboard KPI card displayed
    in evaluation monitoring and reporting views.
    """

    card_id: str

    title: str

    value: float

    formatted_value: str

    unit: str | None = None

    description: str | None = None

    trend_value: float | None = None

    trend_label: str | None = None

    is_positive_trend: bool | None = None

    severity: DashboardSeverity | None = None

    sort_order: int = 0

    def __post_init__(
        self,
    ) -> None:
        DashboardMetricCardValidator.validate(
            card_id=self.card_id,
            title=self.title,
            value=self.value,
            formatted_value=(
                self.formatted_value
            ),
            unit=self.unit,
            description=self.description,
            trend_value=self.trend_value,
            trend_label=self.trend_label,
            is_positive_trend=(
                self.is_positive_trend
            ),
            severity=self.severity,
            sort_order=self.sort_order,
        )

    @property
    def has_trend(
        self,
    ) -> bool:
        return (
            self.trend_value is not None
            or self.trend_label is not None
        )

    @property
    def has_description(
        self,
    ) -> bool:
        return (
            self.description is not None
        )

    @property
    def has_severity(
        self,
    ) -> bool:
        return (
            self.severity is not None
        )