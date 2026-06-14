from __future__ import annotations

from src.evaluation.reporting.renderers.executive_summary_markdown_renderer import ExecutiveSummaryMarkdownRenderer


def test_render_outputs_markdown_sections(executive_summary) -> None:
    markdown = ExecutiveSummaryMarkdownRenderer().render(summary=executive_summary)

    assert markdown.startswith("# Weekly Evaluation")
    assert "## Overall Assessment" in markdown
    assert "| Overall Score | 0.8600 |" in markdown
    assert "- Accuracy improved" in markdown
    assert "## Notes" in markdown
