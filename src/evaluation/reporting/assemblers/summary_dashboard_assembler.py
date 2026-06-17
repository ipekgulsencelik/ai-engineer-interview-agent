from __future__ import annotations

from src.evaluation.reporting.entities.executive_summary import (
    ExecutiveSummary,
)
from src.evaluation.reporting.factories.dashboard_layout_factory import (
    DashboardLayoutFactory,
)
from src.evaluation.reporting.factories.dashboard_widget_factory import (
    DashboardWidgetFactory,
)
from src.evaluation.reporting.entities.chart_data import (
    ChartData,
)
from src.evaluation.reporting.entities.dashboard_layout import (
    DashboardLayout,
)
from src.evaluation.reporting.entities.dashboard_widget import (
    DashboardWidget,
)


class SummaryDashboardAssembler:
    """
    Assembles dashboard layouts from executive summaries.
    """

    def __init__(
        self,
        *,
        layout_factory: DashboardLayoutFactory,
        widget_factory: DashboardWidgetFactory,
    ) -> None:
        self._layout_factory = layout_factory
        self._widget_factory = widget_factory

    def assemble(
        self,
        *,
        dashboard_id: str,
        title: str,
        summary: ExecutiveSummary,
        chart: ChartData | None = None,
        metadata: dict[
            str,
            str,
        ] | None = None,
    ) -> DashboardLayout:
        widgets: list[
            DashboardWidget
        ] = [
            self._widget_factory.create_summary(
                summary=summary,
                order=0,
            ),
            self._widget_factory.create_metric(
                title="Overall Score",
                value=summary.overall_score,
                metric_name="overall_score",
                order=1,
            ),
            self._widget_factory.create_metric(
                title="Pass Rate",
                value=summary.pass_rate,
                metric_name="pass_rate",
                order=2,
            ),
            self._widget_factory.create_metric(
                title="Total Runs",
                value=summary.total_runs,
                metric_name="total_runs",
                order=3,
            ),
        ]

        if chart is not None:
            widgets.append(
                self._widget_factory.create_chart(
                    chart=chart,
                    order=4,
                )
            )

        return self._layout_factory.create(
            dashboard_id=dashboard_id,
            title=title,
            widgets=tuple(
                widgets,
            ),
            metadata=metadata,
        )