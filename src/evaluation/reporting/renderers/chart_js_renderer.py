from __future__ import annotations

from src.evaluation.reporting.renderers.chart_renderer import (
    ChartRenderer,
)
from src.evaluation.reporting.entities.chart_data import (
    ChartData,
)


class ChartJSRenderer(ChartRenderer):
    """
    Renders ChartData as Chart.js payload.
    """

    def render(
        self,
        *,
        chart: ChartData,
    ) -> dict[str, object]:
        return {
            "type": chart.chart_type,
            "data": {
                "labels": list(
                    chart.labels,
                ),
                "datasets": [
                    {
                        "label": (
                            chart.series_name
                            or chart.metric_name
                            or chart.title
                        ),
                        "data": list(
                            chart.scores,
                        ),
                    }
                ],
            },
        }