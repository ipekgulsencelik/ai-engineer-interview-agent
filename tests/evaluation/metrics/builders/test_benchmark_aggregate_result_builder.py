from __future__ import annotations

from datetime import datetime, timezone
from statistics import stdev

import pytest

from src.evaluation.metrics.builders.benchmark_aggregate_result_builder import (
    BenchmarkAggregateResultBuilder,
)
from src.evaluation.metrics.entities.experiment_result_snapshot import (
    ExperimentResultSnapshot,
)
from src.evaluation.metrics.interpreters.benchmark_interpreter import (
    BenchmarkInterpreter,
)
from src.evaluation.metrics.reports.benchmark_evaluation_report import (
    BenchmarkEvaluationReport,
)
from src.evaluation.metrics.value_objects.benchmark_aggregate_result import (
    BenchmarkAggregateResult,
)
from tests.evaluation.metrics.entities.test_benchmark_evaluation_report import (
    _alignment_report,
)


def _snapshot(
    *,
    experiment_id: str,
    score: float,
) -> ExperimentResultSnapshot:
    return ExperimentResultSnapshot(
        experiment_id=experiment_id,
        benchmark_id="benchmark-1",
        benchmark_version="1.0.0",
        dataset_id="dataset-1",
        dataset_version="1.0.0",
        dataset_hash="sha256:abc123",
        model_name="gpt-5",
        metrics_version="1.0.0",
        benchmark_report=BenchmarkEvaluationReport(
            benchmark_id="benchmark-1",
            benchmark_name="AI Engineer Benchmark",
            dataset_id="dataset-1",
            dataset_version="1.0.0",
            model_name="gpt-5",
            evaluator_id="evaluator-1",
            alignment_report=_alignment_report(),
            category_snapshots=(),
            overall_score=score,
            interpretation=BenchmarkInterpreter.interpret(
                benchmark_score=score,
            ),
        ),
        execution_time_seconds=12.5,
        created_at=datetime.now(tz=timezone.utc),
    )


def test_benchmark_aggregate_result_builder_should_build_aggregate_result() -> None:
    scores = (
        0.70,
        0.85,
        0.80,
    )

    aggregate_result = BenchmarkAggregateResultBuilder().build(
        benchmark_id="benchmark-1",
        benchmark_version="1.0.0",
        snapshots=(
            _snapshot(
                experiment_id="experiment-1",
                score=scores[0],
            ),
            _snapshot(
                experiment_id="experiment-2",
                score=scores[1],
            ),
            _snapshot(
                experiment_id="experiment-3",
                score=scores[2],
            ),
        ),
        notes="Aggregate builder test.",
    )

    assert isinstance(aggregate_result, BenchmarkAggregateResult)
    assert aggregate_result.benchmark_id == "benchmark-1"
    assert aggregate_result.benchmark_version == "1.0.0"
    assert aggregate_result.experiment_count == 3
    assert aggregate_result.mean_score == pytest.approx(sum(scores) / len(scores))
    assert aggregate_result.median_score == pytest.approx(0.80)
    assert aggregate_result.min_score == pytest.approx(0.70)
    assert aggregate_result.max_score == pytest.approx(0.85)
    assert aggregate_result.std_deviation == pytest.approx(stdev(scores))
    assert aggregate_result.trend_direction == "improving"
    assert aggregate_result.best_experiment_id == "experiment-2"
    assert aggregate_result.worst_experiment_id == "experiment-1"
    assert aggregate_result.interpretation == "moderate_benchmark"
    assert aggregate_result.notes == "Aggregate builder test."


class _FakeStatisticsCalculator:
    def calculate_scores(
        self,
        *,
        snapshots: tuple[ExperimentResultSnapshot, ...],
    ) -> tuple[float, ...]:
        return (0.25, 0.75)

    def calculate_mean(
        self,
        *,
        scores: tuple[float, ...],
    ) -> float:
        return 0.50

    def calculate_median(
        self,
        *,
        scores: tuple[float, ...],
    ) -> float:
        return 0.50

    def calculate_min(
        self,
        *,
        scores: tuple[float, ...],
    ) -> float:
        return 0.25

    def calculate_max(
        self,
        *,
        scores: tuple[float, ...],
    ) -> float:
        return 0.75

    def calculate_standard_deviation(
        self,
        *,
        scores: tuple[float, ...],
    ) -> float:
        return 0.35

    def find_best_snapshot(
        self,
        *,
        snapshots: tuple[ExperimentResultSnapshot, ...],
    ) -> ExperimentResultSnapshot:
        return snapshots[1]

    def find_worst_snapshot(
        self,
        *,
        snapshots: tuple[ExperimentResultSnapshot, ...],
    ) -> ExperimentResultSnapshot:
        return snapshots[0]


class _FakeTrendDetector:
    def detect(
        self,
        *,
        scores: tuple[float, ...],
    ) -> str:
        return "stable"


class _FakeBenchmarkInterpreter:
    def interpret(
        self,
        *,
        benchmark_score: float,
    ) -> str:
        return f"fake_score_{benchmark_score:.2f}"


def test_benchmark_aggregate_result_builder_should_use_injected_dependencies() -> None:
    aggregate_result = BenchmarkAggregateResultBuilder(
        statistics_calculator=_FakeStatisticsCalculator(),
        trend_detector=_FakeTrendDetector(),
        benchmark_interpreter=_FakeBenchmarkInterpreter(),
    ).build(
        benchmark_id="benchmark-1",
        benchmark_version="1.0.0",
        snapshots=(
            _snapshot(
                experiment_id="experiment-1",
                score=0.10,
            ),
            _snapshot(
                experiment_id="experiment-2",
                score=0.90,
            ),
        ),
    )

    assert aggregate_result.mean_score == pytest.approx(0.50)
    assert aggregate_result.median_score == pytest.approx(0.50)
    assert aggregate_result.min_score == pytest.approx(0.25)
    assert aggregate_result.max_score == pytest.approx(0.75)
    assert aggregate_result.std_deviation == pytest.approx(0.35)
    assert aggregate_result.trend_direction == "stable"
    assert aggregate_result.best_experiment_id == "experiment-2"
    assert aggregate_result.worst_experiment_id == "experiment-1"
    assert aggregate_result.interpretation == "fake_score_0.50"
