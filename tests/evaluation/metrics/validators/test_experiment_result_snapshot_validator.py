from __future__ import annotations

from datetime import datetime, timezone

import pytest

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.metrics.validators.experiment_result_snapshot_validator import (
    ExperimentResultSnapshotValidator,
)
from tests.evaluation.metrics.entities.test_experiment_result_snapshot import (
    _benchmark_report,
)


def test_experiment_result_snapshot_validator_should_validate_successfully() -> None:
    ExperimentResultSnapshotValidator.validate(
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
        created_at=datetime.now(
            tz=timezone.utc,
        ),
        tags=(
            "nightly",
            "regression",
        ),
        notes="Valid.",
    )


def test_experiment_result_snapshot_validator_should_raise_for_invalid_benchmark_report() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="benchmark_report must be BenchmarkEvaluationReport",
    ):
        ExperimentResultSnapshotValidator.validate(
            experiment_id="experiment-1",
            benchmark_id="benchmark-1",
            benchmark_version="1.0.0",
            dataset_id="dataset-1",
            dataset_version="1.0.0",
            dataset_hash="sha256:abc123",
            model_name="gpt-5",
            metrics_version="1.0.0",
            benchmark_report="invalid",  # type: ignore[arg-type]
            execution_time_seconds=12.5,
            created_at=datetime.now(tz=timezone.utc),
            tags=(),
            notes=None,
        )


def test_experiment_result_snapshot_validator_should_raise_for_invalid_tags_type() -> None:
    with pytest.raises(
        EvaluationValidationError,
    ):
        ExperimentResultSnapshotValidator.validate(
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
            tags=["nightly"],  # type: ignore[arg-type]
            notes=None,
        )