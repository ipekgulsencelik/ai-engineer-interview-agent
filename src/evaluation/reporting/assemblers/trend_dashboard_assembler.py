from __future__ import annotations

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
from src.evaluation.reporting.entities.experiment_trend_result import (
    ExperimentTrendResult,
)


class TrendDashboardAssembler:
    """
    Assembles dashboard layouts from experiment trend results.
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
        trend: ExperimentTrendResult,
        chart: ChartData,
        metadata: dict[
            str,
            str,
        ] | None = None,
    ) -> DashboardLayout:
        return self._layout_factory.create(
            dashboard_id=dashboard_id,
            title="Experiment Trend Dashboard",
            widgets=(
                self._widget_factory.create_metric(
                    title="Run Count",
                    value=trend.run_count,
                    metric_name="run_count",
                    order=0,
                ),
                self._widget_factory.create_metric(
                    title="Latest Score",
                    value=trend.latest_overall_score,
                    metric_name="latest_overall_score",
                    order=1,
                ),
                self._widget_factory.create_metric(
                    title="Average Score",
                    value=trend.average_overall_score,
                    metric_name="average_overall_score",
                    order=2,
                ),
                self._widget_factory.create_metric(
                    title="Score Delta",
                    value=trend.overall_score_delta,
                    metric_name="overall_score_delta",
                    order=3,
                ),
                self._widget_factory.create_chart(
                    chart=chart,
                    order=4,
                ),
                self._widget_factory.create_text(
                    title="Trend Interpretation",
                    text=trend.interpretation,
                    order=5,
                ),
            ),
            metadata=metadata,
        )