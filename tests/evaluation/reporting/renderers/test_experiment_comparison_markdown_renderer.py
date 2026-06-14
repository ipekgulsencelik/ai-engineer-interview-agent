from __future__ import annotations

from src.evaluation.reporting.renderers.experiment_comparison_markdown_renderer import ExperimentComparisonMarkdownRenderer


def test_render_outputs_comparison_markdown(experiment_comparison) -> None:
    markdown = ExperimentComparisonMarkdownRenderer().render(comparison=experiment_comparison)

    assert markdown.startswith("# Experiment Comparison Report")
    assert "| Candidate Experiment | Candidate |" in markdown
    assert "Candidate is better." in markdown
