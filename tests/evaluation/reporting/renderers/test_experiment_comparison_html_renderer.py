from __future__ import annotations

from src.evaluation.reporting.renderers.experiment_comparison_html_renderer import ExperimentComparisonHTMLRenderer


def test_render_outputs_comparison_html(experiment_comparison) -> None:
    html = ExperimentComparisonHTMLRenderer().render(comparison=experiment_comparison)

    assert "Experiment Comparison Report" in html
    assert "candidate-exp" in html
    assert "Candidate is better." in html
