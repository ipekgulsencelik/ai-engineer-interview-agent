from __future__ import annotations

from src.evaluation.ops.exporters.html_rendering_utils import (
    HTMLRenderingUtils,
)
from src.evaluation.ops.value_objects.experiment_trend_result import (
    ExperimentTrendResult,
)


class ExperimentTrendHTMLRenderer:
    """
    Renders experiment trend reports as HTML.
    """

    def __init__(
        self,
        *,
        utils: HTMLRenderingUtils | None = None,
    ) -> None:
        self._utils = (
            utils
            or HTMLRenderingUtils()
        )

    def render(
        self,
        *,
        trend: ExperimentTrendResult,
    ) -> str:
        body = "\n".join(
            [
                self._utils.h1(
                    "Experiment Trend Report",
                ),
                self._utils.section(
                    title="Experiment",
                    content=self._utils.table(
                        rows={
                            "Experiment ID": trend.experiment_id,
                            "Experiment Name": trend.experiment_name,
                            "Experiment Version": (
                                trend.experiment_version
                            ),
                            "Run Count": trend.run_count,
                            "First Run ID": trend.first_run_id,
                            "Latest Run ID": trend.latest_run_id,
                        },
                    ),
                ),
                self._utils.section(
                    title="Metrics",
                    content=self._utils.table(
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
                            "First Pass Rate": (
                                trend.first_pass_rate
                            ),
                            "Latest Pass Rate": (
                                trend.latest_pass_rate
                            ),
                            "Pass Rate Delta": (
                                trend.pass_rate_delta
                            ),
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
                ),
                self._utils.section(
                    title="Interpretation",
                    content=self._utils.paragraph(
                        trend.interpretation,
                    ),
                ),
                (
                    ""
                    if trend.notes is None
                    else self._utils.section(
                        title="Notes",
                        content=self._utils.paragraph(
                            trend.notes,
                        ),
                    )
                ),
            ]
        )

        return self._utils.document(
            title="Experiment Trend Report",
            body=body,
        )