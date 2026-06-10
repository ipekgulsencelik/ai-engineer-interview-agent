from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol

from src.evaluation.metrics.calculators.benchmark_aggregate_statistics_calculator import (
    BenchmarkAggregateStatisticsCalculator,
)
from src.evaluation.metrics.detectors.benchmark_trend_detector import (
    BenchmarkTrendDetector,
)
from src.evaluation.metrics.entities.experiment_result_snapshot import (
    ExperimentResultSnapshot,
)
from src.evaluation.metrics.interpreters.benchmark_interpreter import (
    BenchmarkInterpreter,
)
from src.evaluation.metrics.value_objects.benchmark_aggregate_result import (
    BenchmarkAggregateResult,
)


class BenchmarkAggregateStatisticsCalculatorProtocol(Protocol):
    """
    Contract for benchmark aggregate statistics calculators.
    """

    def calculate_scores(
        self,
        *,
        snapshots: Sequence[ExperimentResultSnapshot],
    ) -> tuple[float, ...]: ...

    def calculate_mean(
        self,
        *,
        scores: tuple[float, ...],
    ) -> float: ...

    def calculate_median(
        self,
        *,
        scores: tuple[float, ...],
    ) -> float: ...

    def calculate_min(
        self,
        *,
        scores: tuple[float, ...],
    ) -> float: ...

    def calculate_max(
        self,
        *,
        scores: tuple[float, ...],
    ) -> float: ...

    def calculate_standard_deviation(
        self,
        *,
        scores: tuple[float, ...],
    ) -> float: ...

    def find_best_snapshot(
        self,
        *,
        snapshots: Sequence[ExperimentResultSnapshot],
    ) -> ExperimentResultSnapshot: ...

    def find_worst_snapshot(
        self,
        *,
        snapshots: Sequence[ExperimentResultSnapshot],
    ) -> ExperimentResultSnapshot: ...


class BenchmarkTrendDetectorProtocol(Protocol):
    """
    Contract for benchmark trend detectors.
    """

    def detect(
        self,
        *,
        scores: tuple[float, ...],
    ) -> str: ...


class BenchmarkInterpreterProtocol(Protocol):
    """
    Contract for benchmark score interpreters.
    """

    def interpret(
        self,
        *,
        benchmark_score: float,
    ) -> str: ...


class BenchmarkAggregateResultBuilder:
    """
    Builds BenchmarkAggregateResult instances.
    """

    def __init__(
        self,
        *,
        statistics_calculator: (
            BenchmarkAggregateStatisticsCalculatorProtocol | None
        ) = None,
        trend_detector: BenchmarkTrendDetectorProtocol | None = None,
        benchmark_interpreter: BenchmarkInterpreterProtocol | None = None,
    ) -> None:
        self._statistics_calculator = (
            statistics_calculator or BenchmarkAggregateStatisticsCalculator()
        )
        self._trend_detector = trend_detector or BenchmarkTrendDetector()
        self._benchmark_interpreter = benchmark_interpreter or BenchmarkInterpreter()

    def build(
        self,
        *,
        benchmark_id: str,
        benchmark_version: str,
        snapshots: Sequence[ExperimentResultSnapshot],
        notes: str | None = None,
    ) -> BenchmarkAggregateResult:
        scores = self._statistics_calculator.calculate_scores(
            snapshots=snapshots,
        )

        best_snapshot = self._statistics_calculator.find_best_snapshot(
            snapshots=snapshots,
        )

        worst_snapshot = self._statistics_calculator.find_worst_snapshot(
            snapshots=snapshots,
        )

        mean_score = self._statistics_calculator.calculate_mean(
            scores=scores,
        )

        return BenchmarkAggregateResult(
            benchmark_id=benchmark_id,
            benchmark_version=benchmark_version,
            experiment_count=len(snapshots),
            mean_score=mean_score,
            median_score=self._statistics_calculator.calculate_median(
                scores=scores,
            ),
            min_score=self._statistics_calculator.calculate_min(
                scores=scores,
            ),
            max_score=self._statistics_calculator.calculate_max(
                scores=scores,
            ),
            std_deviation=self._statistics_calculator.calculate_standard_deviation(
                scores=scores,
            ),
            trend_direction=self._trend_detector.detect(
                scores=scores,
            ),
            best_experiment_id=best_snapshot.experiment_id,
            worst_experiment_id=worst_snapshot.experiment_id,
            interpretation=self._benchmark_interpreter.interpret(
                benchmark_score=mean_score,
            ),
            notes=notes,
        )
