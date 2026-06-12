from __future__ import annotations

from datetime import datetime, timezone

import pytest

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.ops.entities.registered_benchmark import RegisteredBenchmark
from tests.evaluation.ops.factories import registered_benchmark


def test_registered_benchmark_should_create_successfully() -> None:
    benchmark = registered_benchmark()

    assert benchmark.identity_key == "benchmark-1:1.0.0"
    assert benchmark.dataset_key == "dataset-1:1.0.0"
    assert benchmark.is_active is True


def test_registered_benchmark_should_raise_for_empty_required_field() -> None:
    with pytest.raises(EvaluationValidationError):
        RegisteredBenchmark(
            benchmark_id="",
            name="AI Engineer Benchmark",
            version="1.0.0",
            dataset_id="dataset-1",
            dataset_version="1.0.0",
        )


def test_registered_benchmark_should_raise_for_invalid_created_at() -> None:
    with pytest.raises(EvaluationValidationError, match="created_at must be datetime"):
        RegisteredBenchmark(
            benchmark_id="benchmark-1",
            name="AI Engineer Benchmark",
            version="1.0.0",
            dataset_id="dataset-1",
            dataset_version="1.0.0",
            created_at="now",  # type: ignore[arg-type]
        )


def test_registered_benchmark_should_accept_datetime_created_at() -> None:
    benchmark = RegisteredBenchmark(
        benchmark_id="benchmark-1",
        name="AI Engineer Benchmark",
        version="1.0.0",
        dataset_id="dataset-1",
        dataset_version="1.0.0",
        created_at=datetime.now(tz=timezone.utc),
    )

    assert benchmark.created_at is not None
