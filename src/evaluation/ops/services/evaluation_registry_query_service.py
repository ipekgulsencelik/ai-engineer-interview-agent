from __future__ import annotations

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.ops.entities.evaluation_registry import (
    EvaluationRegistry,
)
from src.evaluation.ops.entities.registered_benchmark import (
    RegisteredBenchmark,
)


class EvaluationRegistryQueryService:
    """
    Query service for evaluation registries.
    """

    @staticmethod
    def get_benchmark(
        *,
        registry: EvaluationRegistry,
        benchmark_id: str,
        version: str,
    ) -> RegisteredBenchmark:
        benchmark = registry.get(
            benchmark_id=benchmark_id,
            version=version,
        )

        if benchmark is None:
            raise EvaluationValidationError(
                "benchmark is not registered."
            )

        return benchmark