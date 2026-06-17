from __future__ import annotations

from uuid import uuid4

from src.evaluation.reporting.engines.chart_rendering_engine import (
    ChartRenderingEngine,
)
from src.evaluation.reporting.entities.executive_summary import (
    ExecutiveSummary,
)
from src.evaluation.reporting.entities.chart_data import (
    ChartData,
)
from src.evaluation.reporting.entities.dashboard_widget import (
    DashboardWidget,
)


class DashboardWidgetFactory:
    """
    Factory for creating dashboard widgets.
    """

    def __init__(
        self,
        *,
        chart_rendering_engine: ChartRenderingEngine,
    ) -> None:
        self._chart_rendering_engine = chart_rendering_engine

    def create_chart(
        self,
        *,
        chart: ChartData,
        order: int,
    ) -> DashboardWidget:
        return DashboardWidget(
            widget_id=str(
                uuid4(),
            ),
            title=chart.title,
            widget_type="chart",
            data=self._chart_rendering_engine.render(
                chart=chart,
            ),
            payload={
                "chart_type": chart.chart_type,
                "metric_name": chart.metric_name,
                "series_name": chart.series_name,
            },
            order=order,
            width=8,
            height=4,
            description=chart.description,
            group="charts",
            metadata=chart.metadata,
        )

    def create_metric(
        self,
        *,
        title: str,
        value: float | int | None,
        metric_name: str,
        order: int,
    ) -> DashboardWidget:
        return DashboardWidget(
            widget_id=str(
                uuid4(),
            ),
            title=title,
            widget_type="metric",
            data={
                "metric_name": metric_name,
                "value": value,
            },
            payload={
                "metric_name": metric_name,
            },
            order=order,
            width=3,
            height=1,
            group="metrics",
        )

    def create_summary(
        self,
        *,
        summary: ExecutiveSummary,
        order: int,
    ) -> DashboardWidget:
        return DashboardWidget(
            widget_id=str(
                uuid4(),
            ),
            title=summary.title,
            widget_type="summary",
            data={
                "overall_assessment": (
                    summary.overall_assessment
                ),
                "key_findings": list(
                    summary.key_findings,
                ),
                "strengths": list(
                    summary.strengths,
                ),
                "weaknesses": list(
                    summary.weaknesses,
                ),
                "recommendations": list(
                    summary.recommendations,
                ),
                "recommendation": summary.recommendation,
            },
            payload={
                "summary_id": summary.summary_id,
                "trend_direction": (
                    None
                    if summary.trend_direction is None
                    else str(
                        summary.trend_direction,
                    )
                ),
                "risk_level": summary.risk_level,
            },
            order=order,
            width=12,
            height=3,
            group="summary",
            metadata={
                "summary_id": summary.summary_id,
            },
        )

    def create_text(
        self,
        *,
        title: str,
        text: str,
        order: int,
    ) -> DashboardWidget:
        return DashboardWidget(
            widget_id=str(
                uuid4(),
            ),
            title=title,
            widget_type="summary",
            data={
                "text": text,
            },
            payload=None,
            order=order,
            width=12,
            height=2,
            group="summary",
        )