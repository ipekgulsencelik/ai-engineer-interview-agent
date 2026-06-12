from __future__ import annotations

import pytest

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.ops.services.evaluation_registry_query_service import (
    EvaluationRegistryQueryService,
)
from tests.evaluation.ops.factories import evaluation_registry, registered_benchmark


def test_evaluation_registry_query_service_should_get_benchmark() -> None:
    benchmark = registered_benchmark()
    registry = evaluation_registry(benchmarks=(benchmark,))

    assert EvaluationRegistryQueryService.get_benchmark(
        registry=registry,
        benchmark_id="benchmark-1",
        version="1.0.0",
    ) == benchmark


def test_evaluation_registry_query_service_should_raise_for_missing_benchmark() -> None:
    with pytest.raises(EvaluationValidationError, match="not registered"):
        EvaluationRegistryQueryService.get_benchmark(
            registry=evaluation_registry(),
            benchmark_id="missing",
            version="1.0.0",
        )
