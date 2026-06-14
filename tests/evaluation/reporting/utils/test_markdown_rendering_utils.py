from __future__ import annotations

from src.evaluation.reporting.utils.markdown_rendering_utils import MarkdownRenderingUtils


def test_render_kpi_table_formats_values_consistently() -> None:
    rendered = MarkdownRenderingUtils.render_kpi_table(rows={"Score": 0.87654, "Owner": None})

    assert "| Score | 0.8765 |" in rendered
    assert "| Owner | - |" in rendered


def test_render_list_section_handles_empty_and_populated_sections() -> None:
    assert MarkdownRenderingUtils.render_list_section(title="Items", values=()) == "## Items\n_None._"
    assert "- first" in MarkdownRenderingUtils.render_list_section(title="Items", values=("first",))
