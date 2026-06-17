from __future__ import annotations

from src.evaluation.reporting.entities.chart_data import (
    ChartData,
)


class ChartStatisticsBuilder:
    """
    Builds chart statistics payload.
    """

    def build(
        self,
        *,
        chart: ChartData,
    ) -> dict[str, float | int | None]:
        return {
            "count": chart.point_count,
            "average_score": chart.average_score,
            "latest_score": chart.latest_score,
            "max_score": chart.max_score,
            "min_score": chart.min_score,
        }