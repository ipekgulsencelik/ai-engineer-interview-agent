from __future__ import annotations

from datetime import datetime, timezone

import pytest

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.ops.validators.registered_benchmark_validator import (
    RegisteredBenchmarkValidator,
)


def test_registered_benchmark_validator_should_accept_valid_payload() -> None:
    RegisteredBenchmarkValidator.validate(
        benchmark_id="benchmark-1",
        name="AI Engineer Benchmark",
        version="1.0.0",
        dataset_id="dataset-1",
        dataset_version="1.0.0",
        description="Description.",
        owner="ml-platform",
        tags=("nightly",),
        is_active=True,
        created_at=datetime.now(tz=timezone.utc),
        notes="Valid benchmark.",
    )


@pytest.mark.parametrize(
    "field_name",
    [
        "benchmark_id",
        "name",
        "version",
        "dataset_id",
        "dataset_version",
    ],
)
def test_registered_benchmark_validator_should_reject_empty_required_strings(
    field_name: str,
) -> None:
    kwargs = {
        "benchmark_id": "benchmark-1",
        "name": "AI Engineer Benchmark",
        "version": "1.0.0",
        "dataset_id": "dataset-1",
        "dataset_version": "1.0.0",
        "tags": (),
        "is_active": True,
    }
    kwargs[field_name] = ""

    with pytest.raises(EvaluationValidationError):
        RegisteredBenchmarkValidator.validate(**kwargs)


def test_registered_benchmark_validator_should_reject_non_datetime_created_at() -> None:
    with pytest.raises(EvaluationValidationError, match="created_at must be datetime"):
        RegisteredBenchmarkValidator.validate(
            benchmark_id="benchmark-1",
            name="AI Engineer Benchmark",
            version="1.0.0",
            dataset_id="dataset-1",
            dataset_version="1.0.0",
            tags=(),
            is_active=True,
            created_at="2026-01-01",  # type: ignore[arg-type]
        )
