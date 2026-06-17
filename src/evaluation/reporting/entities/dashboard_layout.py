from __future__ import annotations

from dataclasses import dataclass

from src.evaluation.reporting.validators.dashboard_layout_validator import (
    DashboardLayoutValidator,
)
from src.evaluation.reporting.entities.dashboard_widget import (
    DashboardWidget,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class DashboardLayout:
    """
    Immutable dashboard layout aggregate.

    Represents a render-ready dashboard layout
    containing ordered widgets and grid metadata.
    """

    layout_id: str

    dashboard_id: str

    title: str

    widgets: tuple[
        DashboardWidget,
        ...,
    ]

    columns: int = 12

    row_height: int = 120

    gap: int = 16

    compact: bool = False

    responsive: bool = True

    metadata: dict[
        str,
        str,
    ] | None = None

    def __post_init__(
        self,
    ) -> None:
        DashboardLayoutValidator.validate(
            layout_id=self.layout_id,
            dashboard_id=self.dashboard_id,
            title=self.title,
            widgets=self.widgets,
            columns=self.columns,
            row_height=self.row_height,
            gap=self.gap,
            compact=self.compact,
            responsive=self.responsive,
            metadata=self.metadata,
        )

    @property
    def widget_count(
        self,
    ) -> int:
        return len(
            self.widgets,
        )

    @property
    def has_widgets(
        self,
    ) -> bool:
        return bool(
            self.widgets,
        )

    @property
    def is_empty(
        self,
    ) -> bool:
        return not self.widgets

    @property
    def has_metadata(
        self,
    ) -> bool:
        return bool(
            self.metadata,
        )

    @property
    def metric_widgets(
        self,
    ) -> tuple[
        DashboardWidget,
        ...,
    ]:
        return tuple(
            widget
            for widget in self.widgets
            if widget.is_metric
        )

    @property
    def chart_widgets(
        self,
    ) -> tuple[
        DashboardWidget,
        ...,
    ]:
        return tuple(
            widget
            for widget in self.widgets
            if widget.is_chart
        )

    @property
    def table_widgets(
        self,
    ) -> tuple[
        DashboardWidget,
        ...,
    ]:
        return tuple(
            widget
            for widget in self.widgets
            if widget.is_table
        )

    @property
    def summary_widgets(
        self,
    ) -> tuple[
        DashboardWidget,
        ...,
    ]:
        return tuple(
            widget
            for widget in self.widgets
            if widget.is_summary
        )

    @property
    def alert_widgets(
        self,
    ) -> tuple[
        DashboardWidget,
        ...,
    ]:
        return tuple(
            widget
            for widget in self.widgets
            if widget.is_alert
        )

    @property
    def ordered_widgets(
        self,
    ) -> tuple[
        DashboardWidget,
        ...,
    ]:
        return tuple(
            sorted(
                self.widgets,
                key=lambda widget: widget.order,
            )
        )

    @property
    def is_single_column(
        self,
    ) -> bool:
        return (
            self.columns == 1
        )

    @property
    def is_grid(
        self,
    ) -> bool:
        return (
            self.columns > 1
        )