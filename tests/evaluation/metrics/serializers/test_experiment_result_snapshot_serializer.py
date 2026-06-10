from __future__ import annotations

import pytest

from src.evaluation.metrics.serializers.experiment_result_snapshot_serializer import (
    ExperimentResultSnapshotSerializer,
)
from tests.evaluation.metrics.calculators.test_benchmark_aggregate_statistics_calculator import (
    _snapshot,
)
from tests.evaluation.metrics.entities.test_benchmark_evaluation_report import (
    _category_snapshot,
)
from src.evaluation.metrics.reports.benchmark_evaluation_report import (
    BenchmarkEvaluationReport,
)
from tests.evaluation.metrics.entities.test_benchmark_evaluation_report import (
    _alignment_report,
)
from src.evaluation.metrics.entities.experiment_result_snapshot import (
    ExperimentResultSnapshot,
)
from datetime import datetime, timezone


def test_experiment_result_snapshot_serializer_should_serialize_snapshot_without_report_version() -> (
    None
):
    report = BenchmarkEvaluationReport(
        benchmark_id="benchmark-1",
        benchmark_name="AI Engineer Benchmark",
        dataset_id="dataset-1",
        dataset_version="1.0.0",
        model_name="gpt-5",
        evaluator_id="evaluator-1",
        alignment_report=_alignment_report(),
        category_snapshots=(
            _category_snapshot(category="RAG", score=0.90),
            _category_snapshot(category="Agents", score=0.70),
        ),
        overall_score=0.80,
        interpretation="strong_benchmark",
        notes="report notes",
    )
    snapshot = ExperimentResultSnapshot(
        experiment_id="experiment-1",
        benchmark_id="benchmark-1",
        benchmark_version="1.0.0",
        dataset_id="dataset-1",
        dataset_version="1.0.0",
        dataset_hash="sha256:abc123",
        model_name="gpt-5",
        metrics_version="1.0.0",
        benchmark_report=report,
        execution_time_seconds=12.5,
        created_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        tags=("nightly",),
        notes="snapshot notes",
    )

    payload = ExperimentResultSnapshotSerializer.serialize(snapshot=snapshot)

    assert payload["experiment_id"] == "experiment-1"
    assert payload["benchmark_version"] == "1.0.0"
    assert payload["created_at"] == "2026-01-01T00:00:00+00:00"
    assert payload["overall_score"] == pytest.approx(0.80)
    assert payload["tags"] == ["nightly"]
    assert payload["benchmark_report"]["benchmark_id"] == "benchmark-1"
    assert "benchmark_version" not in payload["benchmark_report"]
    assert payload["benchmark_report"]["strongest_category"] == "RAG"
    assert payload["benchmark_report"]["weakest_category"] == "Agents"
    assert len(payload["category_snapshots"]) == 2
    assert payload["category_snapshots"][0]["category"] == "RAG"


def test_experiment_result_snapshot_serializer_should_handle_snapshot_without_categories() -> (
    None
):
    payload = ExperimentResultSnapshotSerializer.serialize(
        snapshot=_snapshot(experiment_id="experiment-empty", score=0.75),
    )

    assert payload["benchmark_report"]["category_count"] == 0
    assert payload["benchmark_report"]["strongest_category"] is None
    assert payload["benchmark_report"]["weakest_category"] is None
    assert payload["category_snapshots"] == []
