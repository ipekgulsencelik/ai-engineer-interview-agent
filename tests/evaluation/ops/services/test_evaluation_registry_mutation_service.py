from __future__ import annotations

import pytest

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.ops.services.evaluation_registry_mutation_service import (
    EvaluationRegistryMutationService,
)
from tests.evaluation.ops.factories import evaluation_registry, registered_benchmark


def test_evaluation_registry_mutation_service_should_register_benchmark() -> None:
    benchmark = registered_benchmark()
    registry = evaluation_registry()

    updated = EvaluationRegistryMutationService.register_benchmark(
        registry=registry,
        benchmark=benchmark,
    )

    assert updated.benchmarks == (benchmark,)
    assert updated.updated_at is not None
    assert registry.benchmarks == ()


def test_evaluation_registry_mutation_service_should_unregister_benchmark() -> None:
    benchmark = registered_benchmark()
    registry = evaluation_registry(benchmarks=(benchmark,))

    updated = EvaluationRegistryMutationService.unregister_benchmark(
        registry=registry,
        benchmark_id="benchmark-1",
        version="1.0.0",
    )

    assert updated.benchmarks == ()


def test_evaluation_registry_mutation_service_should_set_active_state() -> None:
    benchmark = registered_benchmark(is_active=True)
    registry = evaluation_registry(benchmarks=(benchmark,))

    updated = EvaluationRegistryMutationService.set_benchmark_active_state(
        registry=registry,
        benchmark_id="benchmark-1",
        version="1.0.0",
        is_active=False,
    )

    assert updated.benchmarks[0].is_active is False


def test_evaluation_registry_mutation_service_should_reject_locked_registry() -> None:
    with pytest.raises(EvaluationValidationError, match="registry is locked"):
        EvaluationRegistryMutationService.register_benchmark(
            registry=evaluation_registry(is_locked=True),
            benchmark=registered_benchmark(),
        )
