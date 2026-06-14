from __future__ import annotations

from src.evaluation.reporting.writers.markdown_file_writer import MarkdownFileWriter


def test_write_persists_markdown_content(tmp_path) -> None:
    output_path = tmp_path / "report.md"

    result = MarkdownFileWriter.write(content="# Report\n", output_path=output_path)

    assert result == output_path
    assert output_path.read_text(encoding="utf-8") == "# Report\n"
