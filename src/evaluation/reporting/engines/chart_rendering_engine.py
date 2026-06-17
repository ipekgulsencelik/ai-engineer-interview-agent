from __future__ import annotations

from src.evaluation.reporting.builders.base_chart_payload_builder import (
    BaseChartPayloadBuilder,
)
from src.evaluation.reporting.validators.chart_type_validator import (
    ChartTypeValidator,
)
from src.evaluation.reporting.renderers.chart_js_renderer import (
    ChartJSRenderer,
)
from src.evaluation.reporting.renderers.dashboard_card_renderer import (
    DashboardCardRenderer,
)
from src.evaluation.reporting.renderers.plotly_renderer import (
    PlotlyRenderer,
)
from src.evaluation.reporting.renderers.recharts_renderer import (
    RechartsRenderer,
)
from src.evaluation.reporting.entities.chart_data import (
    ChartData,
)


class ChartRenderingEngine:
    """
    Facade for rendering ChartData into different payload formats.
    """

    def __init__(
        self,
        *,
        chart_type_validator: ChartTypeValidator,
        base_payload_builder: BaseChartPayloadBuilder,
        chartjs_renderer: ChartJSRenderer,
        recharts_renderer: RechartsRenderer,
        plotly_renderer: PlotlyRenderer,
        dashboard_card_renderer: DashboardCardRenderer,
    ) -> None:
        self._chart_type_validator = chart_type_validator
        self._base_payload_builder = base_payload_builder
        self._chartjs_renderer = chartjs_renderer
        self._recharts_renderer = recharts_renderer
        self._plotly_renderer = plotly_renderer
        self._dashboard_card_renderer = dashboard_card_renderer

    def render(
        self,
        *,
        chart: ChartData,
    ) -> dict[str, object]:
        self._validate(
            chart=chart,
        )

        return self._base_payload_builder.build(
            chart=chart,
        )

    def render_chartjs(
        self,
        *,
        chart: ChartData,
    ) -> dict[str, object]:
        self._validate(
            chart=chart,
        )

        return self._chartjs_renderer.render(
            chart=chart,
        )

    def render_recharts(
        self,
        *,
        chart: ChartData,
    ) -> dict[str, object]:
        self._validate(
            chart=chart,
        )

        return self._recharts_renderer.render(
            chart=chart,
        )

    def render_plotly(
        self,
        *,
        chart: ChartData,
    ) -> dict[str, object]:
        self._validate(
            chart=chart,
        )

        return self._plotly_renderer.render(
            chart=chart,
        )

    def render_dashboard_card(
        self,
        *,
        chart: ChartData,
    ) -> dict[str, object]:
        self._validate(
            chart=chart,
        )

        return self._dashboard_card_renderer.render(
            chart=chart,
        )

    def _validate(
        self,
        *,
        chart: ChartData,
    ) -> None:
        self._chart_type_validator.validate(
            chart_type=chart.chart_type,
        )