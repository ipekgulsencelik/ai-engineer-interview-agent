from __future__ import annotations

from src.evaluation.reporting.exporters.html_report_exporter import HTMLReportExporter


def test_exporter_renders_and_writes_html(executive_summary, tmp_path) -> None:
    output_path = tmp_path / "summary.html"

    result = HTMLReportExporter().export_executive_summary(
        summary=executive_summary,
        output_path=output_path,
    )

    assert result == output_path
    assert "<!doctype html>" in output_path.read_text(encoding="utf-8")
