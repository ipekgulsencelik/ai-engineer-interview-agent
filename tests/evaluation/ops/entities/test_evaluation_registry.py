from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.ops.entities.evaluation_registry import EvaluationRegistry
from tests.evaluation.ops.factories import evaluation_registry, registered_benchmark


def test_evaluation_registry_should_expose_benchmark_helpers() -> None:
    active = registered_benchmark(benchmark_id="active", is_active=True)
    inactive = registered_benchmark(benchmark_id="inactive", is_active=False)

    registry = evaluation_registry(benchmarks=(active, inactive))

    assert registry.benchmark_count == 2
    assert registry.active_benchmark_count == 1
    assert registry.inactive_benchmark_count == 1
    assert registry.has_benchmarks is True
    assert registry.active_benchmarks == (active,)
    assert registry.inactive_benchmarks == (inactive,)
    assert registry.contains(benchmark_id="active", version="1.0.0") is True
    assert registry.get(benchmark_id="missing", version="1.0.0") is None


def test_evaluation_registry_should_raise_for_duplicate_benchmarks() -> None:
    benchmark = registered_benchmark()

    with pytest.raises(EvaluationValidationError, match="duplicate identity"):
        evaluation_registry(benchmarks=(benchmark, benchmark))


def test_evaluation_registry_should_raise_for_invalid_updated_at_order() -> None:
    created_at = datetime.now(tz=timezone.utc)

    with pytest.raises(EvaluationValidationError, match="earlier than created_at"):
        EvaluationRegistry(
            registry_id="registry-1",
            registry_name="Evaluation Registry",
            version="1.0.0",
            benchmarks=(),
            created_at=created_at,
            updated_at=created_at - timedelta(seconds=1),
        )
