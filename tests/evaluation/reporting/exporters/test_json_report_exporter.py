from __future__ import annotations

import json

from src.evaluation.reporting.exporters.json_report_exporter import JSONReportExporter


def test_exporter_renders_and_writes_json(executive_summary, tmp_path) -> None:
    output_path = tmp_path / "summary.json"

    result = JSONReportExporter().export_executive_summary(
        summary=executive_summary,
        output_path=output_path,
    )

    assert result == output_path
    assert json.loads(output_path.read_text(encoding="utf-8"))["summary_id"] == "summary-1"
