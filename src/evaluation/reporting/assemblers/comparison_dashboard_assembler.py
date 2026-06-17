from __future__ import annotations

from src.evaluation.reporting.factories.dashboard_layout_factory import (
    DashboardLayoutFactory,
)
from src.evaluation.reporting.factories.dashboard_widget_factory import (
    DashboardWidgetFactory,
)
from src.evaluation.reporting.entities.dashboard_layout import (
    DashboardLayout,
)
from src.evaluation.reporting.entities.experiment_comparison_result import (
    ExperimentComparisonResult,
)


class ComparisonDashboardAssembler:
    """
    Assembles dashboard layouts from experiment comparison results.
    """

    def __init__(
        self,
        *,
        layout_factory: DashboardLayoutFactory,
        widget_factory: DashboardWidgetFactory,
    ) -> None:
        self._layout_factory = layout_factory
        self._widget_factory = widget_factory

    def assemble(
        self,
        *,
        dashboard_id: str,
        comparison: ExperimentComparisonResult,
        metadata: dict[
            str,
            str,
        ] | None = None,
    ) -> DashboardLayout:
        return self._layout_factory.create(
            dashboard_id=dashboard_id,
            title="Experiment Comparison Dashboard",
            widgets=(
                self._widget_factory.create_metric(
                    title="Baseline Score",
                    value=comparison.baseline_overall_score,
                    metric_name="baseline_overall_score",
                    order=0,
                ),
                self._widget_factory.create_metric(
                    title="Candidate Score",
                    value=comparison.candidate_overall_score,
                    metric_name="candidate_overall_score",
                    order=1,
                ),
                self._widget_factory.create_metric(
                    title="Score Delta",
                    value=comparison.overall_score_delta,
                    metric_name="overall_score_delta",
                    order=2,
                ),
                self._widget_factory.create_metric(
                    title="Pass Rate Delta",
                    value=comparison.pass_rate_delta,
                    metric_name="pass_rate_delta",
                    order=3,
                ),
                self._widget_factory.create_text(
                    title="Comparison Interpretation",
                    text=comparison.interpretation,
                    order=4,
                ),
            ),
            metadata=metadata,
        )