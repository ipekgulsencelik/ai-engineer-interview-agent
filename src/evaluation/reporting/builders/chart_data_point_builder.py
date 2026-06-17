from __future__ import annotations

from src.evaluation.reporting.entities.chart_data import (
    ChartData,
)


class ChartDataPointBuilder:
    """
    Builds chart data point payloads.
    """

    def build(
        self,
        *,
        chart: ChartData,
    ) -> list[dict[str, object]]:
        return [
            {
                "label": label,
                "score": score,
            }
            for label, score in zip(
                chart.labels,
                chart.scores,
                strict=False,
            )
        ]