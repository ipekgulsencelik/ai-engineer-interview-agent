from __future__ import annotations

from dataclasses import dataclass

from src.evaluation.metrics.validators.benchmark_aggregate_result_validator import (
    BenchmarkAggregateResultValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class BenchmarkAggregateResult:
    """
    Immutable benchmark aggregate result.

    Represents benchmark-level aggregate statistics
    computed across multiple experiment executions.
    """

    benchmark_id: str

    benchmark_version: str

    experiment_count: int

    mean_score: float

    median_score: float

    min_score: float

    max_score: float

    std_deviation: float

    trend_direction: str

    best_experiment_id: str

    worst_experiment_id: str

    interpretation: str

    notes: str | None = None

    def __post_init__(
        self,
    ) -> None:
        BenchmarkAggregateResultValidator.validate(
            benchmark_id=self.benchmark_id,
            benchmark_version=self.benchmark_version,
            experiment_count=self.experiment_count,
            mean_score=self.mean_score,
            median_score=self.median_score,
            min_score=self.min_score,
            max_score=self.max_score,
            std_deviation=self.std_deviation,
            trend_direction=self.trend_direction,
            best_experiment_id=self.best_experiment_id,
            worst_experiment_id=self.worst_experiment_id,
            interpretation=self.interpretation,
            notes=self.notes,
        )

    @property
    def score_range(
        self,
    ) -> float:
        return (
            self.max_score
            - self.min_score
        )

    @property
    def has_variance(
        self,
    ) -> bool:
        return (
            self.std_deviation
            > 0
        )

    @property
    def is_improving(
        self,
    ) -> bool:
        return (
            self.trend_direction
            == "improving"
        )

    @property
    def is_stable(
        self,
    ) -> bool:
        return (
            self.trend_direction
            == "stable"
        )

    @property
    def is_degrading(
        self,
    ) -> bool:
        return (
            self.trend_direction
            == "degrading"
        )