from __future__ import annotations

from pathlib import Path

from src.evaluation.reporting.exporters.pdf_report_exporter import PDFReportExporter


class FakeHTMLExporter:
    def render_executive_summary(self, *, summary) -> str:
        return f"<h1>{summary.title}</h1>"


class FakePDFWriter:
    def __init__(self) -> None:
        self.html: str | None = None

    def write(self, *, html: str, output_path: str | Path) -> Path:
        self.html = html
        path = Path(output_path)
        path.write_bytes(b"%PDF")
        return path


def test_exporter_converts_rendered_html_to_pdf(executive_summary, tmp_path) -> None:
    writer = FakePDFWriter()
    output_path = tmp_path / "summary.pdf"

    result = PDFReportExporter(
        html_exporter=FakeHTMLExporter(),
        pdf_writer=writer,
    ).export_executive_summary(summary=executive_summary, output_path=output_path)

    assert result == output_path
    assert writer.html == "<h1>Weekly Evaluation</h1>"
    assert output_path.read_bytes() == b"%PDF"
