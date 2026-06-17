from __future__ import annotations

from src.evaluation.reporting.renderers.chart_renderer import (
    ChartRenderer,
)
from src.evaluation.reporting.entities.chart_data import (
    ChartData,
)


class DashboardCardRenderer(ChartRenderer):
    """
    Renders ChartData as dashboard metric card payload.
    """

    def render(
        self,
        *,
        chart: ChartData,
    ) -> dict[str, object]:
        return {
            "title": chart.title,
            "metric": chart.metric_name,
            "average_score": chart.average_score,
            "latest_score": chart.latest_score,
            "max_score": chart.max_score,
            "min_score": chart.min_score,
            "trend_direction": chart.trend_direction,
        }