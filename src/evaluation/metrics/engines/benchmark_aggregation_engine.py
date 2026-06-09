from __future__ import annotations

from collections.abc import Sequence

from src.evaluation.metrics.builders.benchmark_aggregate_result_builder import (
    BenchmarkAggregateResultBuilder,
)
from src.evaluation.metrics.entities.experiment_result_snapshot import (
    ExperimentResultSnapshot,
)
from src.evaluation.metrics.validators.benchmark_aggregation_input_validator import (
    BenchmarkAggregationInputValidator,
)
from src.evaluation.metrics.value_objects.benchmark_aggregate_result import (
    BenchmarkAggregateResult,
)


class BenchmarkAggregationEngine:
    """
    Benchmark aggregation orchestration engine.
    """

    @staticmethod
    def aggregate(
        *,
        benchmark_id: str,
        benchmark_version: str,
        snapshots: Sequence[ExperimentResultSnapshot],
        notes: str | None = None,
    ) -> BenchmarkAggregateResult:
        BenchmarkAggregationInputValidator.validate(
            snapshots=snapshots,
        )

        return BenchmarkAggregateResultBuilder.build(
            benchmark_id=benchmark_id,
            benchmark_version=benchmark_version,
            snapshots=snapshots,
            notes=notes,
        )