from __future__ import annotations

from datetime import datetime, timezone
from statistics import stdev

import pytest

from src.evaluation.metrics.calculators.benchmark_aggregate_statistics_calculator import (
    BenchmarkAggregateStatisticsCalculator,
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


def test_benchmark_aggregate_statistics_calculator_should_extract_scores() -> None:
    snapshots = (
        _snapshot(
            experiment_id="experiment-1",
            score=0.70,
        ),
        _snapshot(
            experiment_id="experiment-2",
            score=0.85,
        ),
        _snapshot(
            experiment_id="experiment-3",
            score=0.80,
        ),
    )

    scores = BenchmarkAggregateStatisticsCalculator.calculate_scores(
        snapshots=snapshots,
    )

    assert scores == (
        0.70,
        0.85,
        0.80,
    )


def test_benchmark_aggregate_statistics_calculator_should_calculate_summary_statistics() -> (
    None
):
    scores = (
        0.70,
        0.85,
        0.80,
        0.90,
    )

    assert BenchmarkAggregateStatisticsCalculator.calculate_mean(
        scores=scores,
    ) == pytest.approx(0.8125)
    assert BenchmarkAggregateStatisticsCalculator.calculate_median(
        scores=scores,
    ) == pytest.approx(0.825)
    assert BenchmarkAggregateStatisticsCalculator.calculate_min(
        scores=scores,
    ) == pytest.approx(0.70)
    assert BenchmarkAggregateStatisticsCalculator.calculate_max(
        scores=scores,
    ) == pytest.approx(0.90)
    assert BenchmarkAggregateStatisticsCalculator.calculate_standard_deviation(
        scores=scores,
    ) == pytest.approx(stdev(scores))


def test_benchmark_aggregate_statistics_calculator_should_return_zero_stdev_for_single_score() -> (
    None
):
    assert BenchmarkAggregateStatisticsCalculator.calculate_standard_deviation(
        scores=(0.80,),
    ) == pytest.approx(0.0)


def test_benchmark_aggregate_statistics_calculator_should_find_best_and_worst_snapshots() -> (
    None
):
    snapshots = (
        _snapshot(
            experiment_id="experiment-1",
            score=0.70,
        ),
        _snapshot(
            experiment_id="experiment-2",
            score=0.85,
        ),
        _snapshot(
            experiment_id="experiment-3",
            score=0.65,
        ),
    )

    best_snapshot = BenchmarkAggregateStatisticsCalculator.find_best_snapshot(
        snapshots=snapshots,
    )
    worst_snapshot = BenchmarkAggregateStatisticsCalculator.find_worst_snapshot(
        snapshots=snapshots,
    )

    assert best_snapshot.experiment_id == "experiment-2"
    assert best_snapshot.overall_score == pytest.approx(0.85)
    assert worst_snapshot.experiment_id == "experiment-3"
    assert worst_snapshot.overall_score == pytest.approx(0.65)
