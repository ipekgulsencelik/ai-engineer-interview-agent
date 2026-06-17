from __future__ import annotations

from src.evaluation.reporting.renderers.chart_renderer import (
    ChartRenderer,
)
from src.evaluation.reporting.entities.chart_data import (
    ChartData,
)


class PlotlyRenderer(ChartRenderer):
    """
    Renders ChartData as Plotly payload.
    """

    def render(
        self,
        *,
        chart: ChartData,
    ) -> dict[str, object]:
        return {
            "data": [
                {
                    "type": chart.chart_type,
                    "x": list(
                        chart.labels,
                    ),
                    "y": list(
                        chart.scores,
                    ),
                    "name": (
                        chart.series_name
                        or chart.metric_name
                        or chart.title
                    ),
                }
            ],
            "layout": {
                "title": chart.title,
                "xaxis": {
                    "title": chart.x_axis_label,
                },
                "yaxis": {
                    "title": chart.y_axis_label,
                },
            },
        }