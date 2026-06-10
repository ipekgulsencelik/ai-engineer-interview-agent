from __future__ import annotations

import pytest

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.metrics.engines.benchmark_aggregation_engine import (
    BenchmarkAggregationEngine,
)
from src.evaluation.metrics.value_objects.benchmark_aggregate_result import (
    BenchmarkAggregateResult,
)
from tests.evaluation.metrics.calculators.test_benchmark_aggregate_statistics_calculator import (
    _snapshot,
)


def test_benchmark_aggregation_engine_should_validate_and_aggregate_snapshots() -> None:
    result = BenchmarkAggregationEngine().aggregate(
        benchmark_id="benchmark-1",
        benchmark_version="1.0.0",
        snapshots=(
            _snapshot(experiment_id="experiment-1", score=0.70),
            _snapshot(experiment_id="experiment-2", score=0.90),
        ),
        notes="aggregation engine test",
    )

    assert isinstance(result, BenchmarkAggregateResult)
    assert result.experiment_count == 2
    assert result.mean_score == pytest.approx(0.80)
    assert result.best_experiment_id == "experiment-2"
    assert result.worst_experiment_id == "experiment-1"
    assert result.trend_direction == "improving"
    assert result.notes == "aggregation engine test"


def test_benchmark_aggregation_engine_should_raise_for_empty_snapshots() -> None:
    with pytest.raises(EvaluationValidationError, match="snapshots cannot be empty"):
        BenchmarkAggregationEngine().aggregate(
            benchmark_id="benchmark-1",
            benchmark_version="1.0.0",
            snapshots=(),
        )


class _FakeAggregateResultBuilder:
    def __init__(self) -> None:
        self.received_notes: str | None = None

    def build(
        self,
        *,
        benchmark_id: str,
        benchmark_version: str,
        snapshots,
        notes: str | None = None,
    ) -> BenchmarkAggregateResult:
        self.received_notes = notes
        return BenchmarkAggregateResult(
            benchmark_id=benchmark_id,
            benchmark_version=benchmark_version,
            experiment_count=len(snapshots),
            mean_score=0.50,
            median_score=0.50,
            min_score=0.25,
            max_score=0.75,
            std_deviation=0.10,
            trend_direction="stable",
            best_experiment_id="experiment-2",
            worst_experiment_id="experiment-1",
            interpretation="fake_benchmark",
            notes=notes,
        )


def test_benchmark_aggregation_engine_should_use_injected_builder() -> None:
    builder = _FakeAggregateResultBuilder()

    result = BenchmarkAggregationEngine(result_builder=builder).aggregate(
        benchmark_id="benchmark-1",
        benchmark_version="1.0.0",
        snapshots=(
            _snapshot(experiment_id="experiment-1", score=0.70),
            _snapshot(experiment_id="experiment-2", score=0.90),
        ),
        notes="injected builder",
    )

    assert result.interpretation == "fake_benchmark"
    assert result.trend_direction == "stable"
    assert result.notes == "injected builder"
    assert builder.received_notes == "injected builder"
