from __future__ import annotations

from src.evaluation.reporting.writers.json_file_writer import JSONFileWriter


def test_write_persists_json_content(tmp_path) -> None:
    output_path = tmp_path / "report.json"

    result = JSONFileWriter.write(content='{"ok": true}\n', output_path=output_path)

    assert result == output_path
    assert output_path.read_text(encoding="utf-8") == '{"ok": true}\n'
