from __future__ import annotations

from src.evaluation.reporting.exporters.markdown_report_exporter import MarkdownReportExporter


def test_exporter_renders_and_writes_markdown(executive_summary, tmp_path) -> None:
    output_path = tmp_path / "summary.md"

    result = MarkdownReportExporter().export_executive_summary(
        summary=executive_summary,
        output_path=output_path,
    )

    assert result == output_path
    assert "# Weekly Evaluation" in output_path.read_text(encoding="utf-8")
