from __future__ import annotations

from src.evaluation.reporting.renderers.experiment_trend_markdown_renderer import ExperimentTrendMarkdownRenderer


def test_render_outputs_trend_markdown(experiment_trend) -> None:
    markdown = ExperimentTrendMarkdownRenderer().render(trend=experiment_trend)

    assert markdown.startswith("# Experiment Trend Report")
    assert "| Experiment ID | exp-1 |" in markdown
    assert "| Latest Overall Score | 0.9000 |" in markdown
    assert "Quality improved." in markdown
