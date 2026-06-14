from __future__ import annotations

from src.evaluation.reporting.writers.html_file_writer import HTMLFileWriter


def test_write_persists_html_content(tmp_path) -> None:
    output_path = tmp_path / "report.html"

    result = HTMLFileWriter.write(content="<h1>Report</h1>", output_path=output_path)

    assert result == output_path
    assert output_path.read_text(encoding="utf-8") == "<h1>Report</h1>"
