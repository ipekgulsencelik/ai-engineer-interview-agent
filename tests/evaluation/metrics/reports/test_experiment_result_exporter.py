from __future__ import annotations

import json

from src.evaluation.metrics.reports.experiment_result_exporter import (
    ExperimentResultExporter,
)
from tests.evaluation.metrics.calculators.test_benchmark_aggregate_statistics_calculator import (
    _snapshot,
)


def test_experiment_result_exporter_should_write_deterministic_json(tmp_path) -> None:
    output_path = tmp_path / "nested" / "experiment.json"

    result_path = ExperimentResultExporter().export(
        snapshot=_snapshot(experiment_id="experiment-1", score=0.80),
        output_path=output_path,
    )

    assert result_path == output_path
    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert payload["experiment_id"] == "experiment-1"
    assert payload["overall_score"] == 0.80
    assert payload["benchmark_report"]["benchmark_id"] == "benchmark-1"
