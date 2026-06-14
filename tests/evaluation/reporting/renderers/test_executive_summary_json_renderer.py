from __future__ import annotations

import json

from src.evaluation.reporting.renderers.executive_summary_json_renderer import ExecutiveSummaryJSONRenderer


def test_render_outputs_summary_json(executive_summary) -> None:
    payload = json.loads(ExecutiveSummaryJSONRenderer().render(summary=executive_summary))

    assert payload["summary_id"] == "summary-1"
    assert payload["title"] == "Weekly Evaluation"
    assert payload["trend_direction"] == "improving"
    assert payload["key_findings"] == ["Accuracy improved"]
