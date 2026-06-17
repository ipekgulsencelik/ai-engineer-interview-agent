from __future__ import annotations

from src.evaluation.reporting.builders.chart_data_point_builder import (
    ChartDataPointBuilder,
)
from src.evaluation.reporting.renderers.chart_renderer import (
    ChartRenderer,
)
from src.evaluation.reporting.entities.chart_data import (
    ChartData,
)


class RechartsRenderer(ChartRenderer):
    """
    Renders ChartData as Recharts payload.
    """

    def __init__(
        self,
        *,
        data_point_builder: ChartDataPointBuilder,
    ) -> None:
        self._data_point_builder = data_point_builder

    def render(
        self,
        *,
        chart: ChartData,
    ) -> dict[str, object]:
        return {
            "chartType": chart.chart_type,
            "title": chart.title,
            "seriesName": chart.series_name,
            "metricName": chart.metric_name,
            "xAxisLabel": chart.x_axis_label,
            "yAxisLabel": chart.y_axis_label,
            "data": self._data_point_builder.build(
                chart=chart,
            ),
        }