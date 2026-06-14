from __future__ import annotations

import json

from src.evaluation.reporting.renderers.experiment_trend_json_renderer import ExperimentTrendJSONRenderer


def test_render_outputs_trend_json(experiment_trend) -> None:
    payload = json.loads(ExperimentTrendJSONRenderer().render(trend=experiment_trend))

    assert payload["experiment_id"] == "exp-1"
    assert payload["latest_overall_score"] == 0.9
    assert payload["trend_direction"] == "improving"
