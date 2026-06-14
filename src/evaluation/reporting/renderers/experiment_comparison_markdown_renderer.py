from __future__ import annotations

from src.evaluation.reporting.utils.markdown_rendering_utils import (
    MarkdownRenderingUtils,
)
from src.evaluation.reporting.entities.experiment_comparison_result import (
    ExperimentComparisonResult,
)


class ExperimentComparisonMarkdownRenderer:
    """
    Renders experiment comparison reports as Markdown.
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
        comparison: ExperimentComparisonResult,
    ) -> str:
        sections = [
            "# Experiment Comparison Report",
            "",
            "## Compared Runs",
            self._utils.render_kpi_table(
                rows={
                    "Baseline Run ID": comparison.baseline_run_id,
                    "Candidate Run ID": comparison.candidate_run_id,
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
            "",
            "## Metrics",
            self._utils.render_kpi_table(
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
            "",
            "## Interpretation",
            comparison.interpretation,
        ]

        if comparison.notes is not None:
            sections.extend(
                [
                    "",
                    "## Notes",
                    comparison.notes,
                ]
            )

        return "\n".join(
            sections,
        ).strip() + "\n"