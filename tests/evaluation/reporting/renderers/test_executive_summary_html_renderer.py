from __future__ import annotations

from src.evaluation.reporting.renderers.executive_summary_html_renderer import ExecutiveSummaryHTMLRenderer


def test_render_outputs_summary_html_document(executive_summary) -> None:
    html = ExecutiveSummaryHTMLRenderer().render(summary=executive_summary)

    assert "<!doctype html>" in html
    assert "Weekly Evaluation" in html
    assert "Accuracy improved" in html
    assert "Ready for review." in html
