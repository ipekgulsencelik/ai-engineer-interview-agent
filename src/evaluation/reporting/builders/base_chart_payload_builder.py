from __future__ import annotations

from src.evaluation.reporting.builders.chart_data_point_builder import (
    ChartDataPointBuilder,
)
from src.evaluation.reporting.builders.chart_statistics_builder import (
    ChartStatisticsBuilder,
)
from src.evaluation.reporting.entities.chart_data import (
    ChartData,
)


class BaseChartPayloadBuilder:
    """
    Builds renderer-ready generic chart payload.
    """

    def __init__(
        self,
        *,
        data_point_builder: ChartDataPointBuilder,
        statistics_builder: ChartStatisticsBuilder,
    ) -> None:
        self._data_point_builder = data_point_builder
        self._statistics_builder = statistics_builder

    def build(
        self,
        *,
        chart: ChartData,
    ) -> dict[str, object]:
        return {
            "title": chart.title,
            "chart_type": chart.chart_type,
            "series_name": chart.series_name,
            "metric_name": chart.metric_name,
            "description": chart.description,
            "trend_direction": chart.trend_direction,
            "average_score": chart.average_score,
            "x_axis_label": chart.x_axis_label,
            "y_axis_label": chart.y_axis_label,
            "data": self._data_point_builder.build(
                chart=chart,
            ),
            "statistics": self._statistics_builder.build(
                chart=chart,
            ),
            "metadata": chart.metadata or {},
        }