from __future__ import annotations

from src.evaluation.reporting.utils.html_rendering_utils import (
    HTMLRenderingUtils,
)
from src.evaluation.tracking.entities.experiment_comparison_result import (
    ExperimentComparisonResult,
)


class ExperimentComparisonHTMLRenderer:
    """
    Renders experiment comparison reports as HTML.
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
        comparison: ExperimentComparisonResult,
    ) -> str:
        body = "\n".join(
            [
                self._utils.h1(
                    "Experiment Comparison Report",
                ),
                self._utils.section(
                    title="Compared Runs",
                    content=self._utils.table(
                        rows={
                            "Baseline Run ID": (
                                comparison.baseline_run_id
                            ),
                            "Candidate Run ID": (
                                comparison.candidate_run_id
                            ),
                            "Baseline Experiment": (
                                comparison.baseline_experiment_name
                            ),
                            "Candidate Experiment": (
                                comparison.candidate_experiment_name
                            ),
                            "Baseline Version": (
                                comparison.baseline_experiment_version
                            ),
                            "Candidate Version": (
                                comparison.candidate_experiment_version
                            ),
                        },
                    ),
                ),
                self._utils.section(
                    title="Metrics",
                    content=self._utils.table(
                        rows={
                            "Baseline Overall Score": (
                                comparison.baseline_overall_score
                            ),
                            "Candidate Overall Score": (
                                comparison.candidate_overall_score
                            ),
                            "Overall Score Delta": (
                                comparison.overall_score_delta
                            ),
                            "Baseline Pass Rate": (
                                comparison.baseline_pass_rate
                            ),
                            "Candidate Pass Rate": (
                                comparison.candidate_pass_rate
                            ),
                            "Pass Rate Delta": (
                                comparison.pass_rate_delta
                            ),
                            "Baseline Sample Count": (
                                comparison.baseline_sample_count
                            ),
                            "Candidate Sample Count": (
                                comparison.candidate_sample_count
                            ),
                            "Sample Count Delta": (
                                comparison.sample_count_delta
                            ),
                            "Winner Experiment ID": (
                                comparison.winner_experiment_id
                            ),
                            "Winning Run ID": (
                                comparison.winning_run_id
                            ),
                        },
                    ),
                ),
                self._utils.section(
                    title="Interpretation",
                    content=self._utils.paragraph(
                        comparison.interpretation,
                    ),
                ),
                (
                    ""
                    if comparison.notes is None
                    else self._utils.section(
                        title="Notes",
                        content=self._utils.paragraph(
                            comparison.notes,
                        ),
                    )
                ),
            ]
        )

        return self._utils.document(
            title="Experiment Comparison Report",
            body=body,
        )