from __future__ import annotations

from src.evaluation.reporting.assemblers.comparison_dashboard_assembler import (
    ComparisonDashboardAssembler,
)
from src.evaluation.reporting.assemblers.summary_dashboard_assembler import (
    SummaryDashboardAssembler,
)
from src.evaluation.reporting.assemblers.trend_dashboard_assembler import (
    TrendDashboardAssembler,
)
from src.evaluation.reporting.entities.executive_summary import (
    ExecutiveSummary,
)
from src.evaluation.reporting.factories.dashboard_layout_factory import (
    DashboardLayoutFactory,
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
from src.evaluation.reporting.entities.experiment_comparison_result import (
    ExperimentComparisonResult,
)
from src.evaluation.reporting.entities.experiment_trend_result import (
    ExperimentTrendResult,
)


class InteractiveDashboardBuilder:
    """
    Facade for building interactive dashboard layouts.
    """

    def __init__(
        self,
        *,
        layout_factory: DashboardLayoutFactory,
        summary_assembler: SummaryDashboardAssembler,
        trend_assembler: TrendDashboardAssembler,
        comparison_assembler: ComparisonDashboardAssembler,
    ) -> None:
        self._layout_factory = layout_factory
        self._summary_assembler = summary_assembler
        self._trend_assembler = trend_assembler
        self._comparison_assembler = comparison_assembler

    def build(
        self,
        *,
        dashboard_id: str,
        title: str,
        widgets: tuple[
            DashboardWidget,
            ...,
        ],
        columns: int = 12,
        row_height: int = 120,
        gap: int = 16,
        compact: bool = False,
        responsive: bool = True,
        metadata: dict[
            str,
            str,
        ] | None = None,
    ) -> DashboardLayout:
        return self._layout_factory.create(
            dashboard_id=dashboard_id,
            title=title,
            widgets=widgets,
            columns=columns,
            row_height=row_height,
            gap=gap,
            compact=compact,
            responsive=responsive,
            metadata=metadata,
        )

    def build_from_summary(
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
        return self._summary_assembler.assemble(
            dashboard_id=dashboard_id,
            title=title,
            summary=summary,
            chart=chart,
            metadata=metadata,
        )

    def build_from_trend(
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
        return self._trend_assembler.assemble(
            dashboard_id=dashboard_id,
            trend=trend,
            chart=chart,
            metadata=metadata,
        )

    def build_from_comparison(
        self,
        *,
        dashboard_id: str,
        comparison: ExperimentComparisonResult,
        metadata: dict[
            str,
            str,
        ] | None = None,
    ) -> DashboardLayout:
        return self._comparison_assembler.assemble(
            dashboard_id=dashboard_id,
            comparison=comparison,
            metadata=metadata,
        )