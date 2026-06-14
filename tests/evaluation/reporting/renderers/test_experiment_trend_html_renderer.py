from __future__ import annotations

from src.evaluation.reporting.renderers.experiment_trend_html_renderer import ExperimentTrendHTMLRenderer


def test_render_outputs_trend_html(experiment_trend) -> None:
    html = ExperimentTrendHTMLRenderer().render(trend=experiment_trend)

    assert "Experiment Trend Report" in html
    assert "RAG Quality" in html
    assert "Quality improved." in html
