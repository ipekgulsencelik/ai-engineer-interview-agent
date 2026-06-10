from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timezone

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.ops.entities.evaluation_registry import (
    EvaluationRegistry,
)
from src.evaluation.ops.entities.registered_benchmark import (
    RegisteredBenchmark,
)
from src.evaluation.ops.services.evaluation_registry_lock_service import (
    EvaluationRegistryLockService,
)


class EvaluationRegistryMutationService:
    """
    Mutation service for immutable evaluation registry snapshots.
    """

    @staticmethod
    def register_benchmark(
        *,
        registry: EvaluationRegistry,
        benchmark: RegisteredBenchmark,
    ) -> EvaluationRegistry:
        EvaluationRegistryLockService.ensure_unlocked(
            registry=registry,
        )

        if registry.contains(
            benchmark_id=benchmark.benchmark_id,
            version=benchmark.version,
        ):
            raise EvaluationValidationError(
                "benchmark is already registered."
            )

        return replace(
            registry,
            benchmarks=(
                *registry.benchmarks,
                benchmark,
            ),
            updated_at=datetime.now(tz=timezone.utc),
        )

    @staticmethod
    def unregister_benchmark(
        *,
        registry: EvaluationRegistry,
        benchmark_id: str,
        version: str,
    ) -> EvaluationRegistry:
        EvaluationRegistryLockService.ensure_unlocked(
            registry=registry,
        )

        if not registry.contains(
            benchmark_id=benchmark_id,
            version=version,
        ):
            raise EvaluationValidationError(
                "benchmark is not registered."
            )

        return replace(
            registry,
            benchmarks=tuple(
                benchmark
                for benchmark in registry.benchmarks
                if not (
                    benchmark.benchmark_id == benchmark_id
                    and benchmark.version == version
                )
            ),
            updated_at=datetime.now(tz=timezone.utc),
        )

    @staticmethod
    def set_benchmark_active_state(
        *,
        registry: EvaluationRegistry,
        benchmark_id: str,
        version: str,
        is_active: bool,
    ) -> EvaluationRegistry:
        EvaluationRegistryLockService.ensure_unlocked(
            registry=registry,
        )

        if not registry.contains(
            benchmark_id=benchmark_id,
            version=version,
        ):
            raise EvaluationValidationError(
                "benchmark is not registered."
            )

        return replace(
            registry,
            benchmarks=tuple(
                replace(
                    benchmark,
                    is_active=is_active,
                )
                if (
                    benchmark.benchmark_id == benchmark_id
                    and benchmark.version == version
                )
                else benchmark
                for benchmark in registry.benchmarks
            ),
            updated_at=datetime.now(tz=timezone.utc),
        )