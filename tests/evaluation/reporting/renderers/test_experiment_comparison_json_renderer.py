from __future__ import annotations

import json

from src.evaluation.reporting.renderers.experiment_comparison_json_renderer import ExperimentComparisonJSONRenderer


def test_render_outputs_comparison_json(experiment_comparison) -> None:
    payload = json.loads(ExperimentComparisonJSONRenderer().render(comparison=experiment_comparison))

    assert payload["candidate_experiment_id"] == "candidate-exp"
    assert payload["overall_score_delta"] == 0.13
    assert payload["winner_experiment_id"] == "candidate-exp"
