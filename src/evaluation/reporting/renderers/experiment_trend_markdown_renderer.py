from __future__ import annotations

from src.evaluation.ops.exporters.markdown_rendering_utils import (
    MarkdownRenderingUtils,
)
from src.evaluation.ops.value_objects.experiment_trend_result import (
    ExperimentTrendResult,
)


class ExperimentTrendMarkdownRenderer:
    """
    Renders experiment trend reports as Markdown.
    """

    def __init__(
        self,
        *,
        utils: MarkdownRenderingUtils | None = None,
    ) -> None:
        self._utils = (
            utils
            or MarkdownRenderingUtils()
        )

    def render(
        self,
        *,
        trend: ExperimentTrendResult,
    ) -> str:
        sections = [
            "# Experiment Trend Report",
            "",
            "## Experiment",
            self._utils.render_kpi_table(
                rows={
                    "Experiment ID": trend.experiment_id,
                    "Experiment Name": trend.experiment_name,
                    "Experiment Version": trend.experiment_version,
                    "Run Count": trend.run_count,
                    "First Run ID": trend.first_run_id,
                    "Latest Run ID": trend.latest_run_id,
                },
            ),
            "",
            "## Metrics",
            self._utils.render_kpi_table(
                rows={
                    "First Overall Score": (
                        trend.first_overall_score
                    ),
                    "Latest Overall Score": (
                        trend.latest_overall_score
                    ),
                    "Average Overall Score": (
                        trend.average_overall_score
                    ),
                    "Overall Score Delta": (
                        trend.overall_score_delta
                    ),
                    "First Pass Rate": trend.first_pass_rate,
                    "Latest Pass Rate": trend.latest_pass_rate,
                    "Pass Rate Delta": trend.pass_rate_delta,
                    "Best Run ID": trend.best_run_id,
                    "Best Overall Score": (
                        trend.best_overall_score
                    ),
                    "Worst Run ID": trend.worst_run_id,
                    "Worst Overall Score": (
                        trend.worst_overall_score
                    ),
                    "Trend Direction": str(
                        trend.trend_direction,
                    ),
                },
            ),
            "",
            "## Interpretation",
            trend.interpretation,
        ]

        if trend.notes is not None:
            sections.extend(
                [
                    "",
                    "## Notes",
                    trend.notes,
                ]
            )

        return "\n".join(
            sections,
        ).strip() + "\n"