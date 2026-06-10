from __future__ import annotations

from datetime import datetime, timezone

import pytest

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.metrics.entities.experiment_result_snapshot import (
    ExperimentResultSnapshot,
)
from tests.evaluation.metrics.entities.test_benchmark_evaluation_report import (
    _alignment_report,
    _category_snapshot,
)
from src.evaluation.metrics.reports.benchmark_evaluation_report import (
    BenchmarkEvaluationReport,
)


def _benchmark_report() -> BenchmarkEvaluationReport:
    return BenchmarkEvaluationReport(
        benchmark_id="benchmark-1",
        benchmark_name="AI Engineer Benchmark",
        dataset_id="dataset-1",
        dataset_version="1.0.0",
        model_name="gpt-5",
        evaluator_id="evaluator-1",
        alignment_report=_alignment_report(),
        category_snapshots=(
            _category_snapshot(
                category="RAG",
                score=0.90,
            ),
            _category_snapshot(
                category="Agents",
                score=0.70,
            ),
        ),
        overall_score=0.80,
        interpretation="strong_benchmark",
    )


def test_experiment_result_snapshot_should_create_successfully() -> None:
    created_at = datetime.now(
        tz=timezone.utc,
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
        benchmark_report=_benchmark_report(),
        execution_time_seconds=12.5,
        created_at=created_at,
        tags=(
            "nightly",
            "regression",
        ),
        notes="Valid experiment snapshot.",
    )

    assert snapshot.experiment_id == "experiment-1"
    assert snapshot.benchmark_id == "benchmark-1"
    assert snapshot.dataset_hash == "sha256:abc123"
    assert snapshot.metrics_version == "1.0.0"
    assert snapshot.overall_score == 0.80
    assert snapshot.benchmark_score == 0.80
    assert snapshot.interpretation == "strong_benchmark"
    assert snapshot.category_count == 2
    assert snapshot.sample_count == 8
    assert snapshot.strongest_category.category == "RAG"
    assert snapshot.weakest_category.category == "Agents"
    assert snapshot.benchmark_name == "AI Engineer Benchmark"
    assert snapshot.tags == (
        "nightly",
        "regression",
    )
    assert snapshot.notes == "Valid experiment snapshot."


@pytest.mark.parametrize(
    "field_name",
    [
        "experiment_id",
        "benchmark_id",
        "benchmark_version",
        "dataset_id",
        "dataset_version",
        "dataset_hash",
        "model_name",
        "metrics_version",
    ],
)
def test_experiment_result_snapshot_should_raise_for_empty_string_fields(
    field_name: str,
) -> None:
    kwargs = {
        "experiment_id": "experiment-1",
        "benchmark_id": "benchmark-1",
        "benchmark_version": "1.0.0",
        "dataset_id": "dataset-1",
        "dataset_version": "1.0.0",
        "dataset_hash": "sha256:abc123",
        "model_name": "gpt-5",
        "metrics_version": "1.0.0",
        "benchmark_report": _benchmark_report(),
        "execution_time_seconds": 12.5,
        "created_at": datetime.now(tz=timezone.utc),
        "tags": (),
        "notes": None,
    }
    kwargs[field_name] = ""

    with pytest.raises(
        EvaluationValidationError,
    ):
        ExperimentResultSnapshot(**kwargs)


def test_experiment_result_snapshot_should_raise_for_negative_execution_time() -> None:
    with pytest.raises(
        EvaluationValidationError,
    ):
        ExperimentResultSnapshot(
            experiment_id="experiment-1",
            benchmark_id="benchmark-1",
            benchmark_version="1.0.0",
            dataset_id="dataset-1",
            dataset_version="1.0.0",
            dataset_hash="sha256:abc123",
            model_name="gpt-5",
            metrics_version="1.0.0",
            benchmark_report=_benchmark_report(),
            execution_time_seconds=-1.0,
            created_at=datetime.now(tz=timezone.utc),
        )


def test_experiment_result_snapshot_should_raise_for_invalid_created_at() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="created_at must be datetime",
    ):
        ExperimentResultSnapshot(
            experiment_id="experiment-1",
            benchmark_id="benchmark-1",
            benchmark_version="1.0.0",
            dataset_id="dataset-1",
            dataset_version="1.0.0",
            dataset_hash="sha256:abc123",
            model_name="gpt-5",
            metrics_version="1.0.0",
            benchmark_report=_benchmark_report(),
            execution_time_seconds=12.5,
            created_at="2026-01-01",  # type: ignore[arg-type]
        )


def test_experiment_result_snapshot_should_be_immutable() -> None:
    snapshot = ExperimentResultSnapshot(
        experiment_id="experiment-1",
        benchmark_id="benchmark-1",
        benchmark_version="1.0.0",
        dataset_id="dataset-1",
        dataset_version="1.0.0",
        dataset_hash="sha256:abc123",
        model_name="gpt-5",
        metrics_version="1.0.0",
        benchmark_report=_benchmark_report(),
        execution_time_seconds=12.5,
        created_at=datetime.now(tz=timezone.utc),
    )

    with pytest.raises(
        AttributeError,
    ):
        snapshot.experiment_id = "changed"  # type: ignore[misc]
