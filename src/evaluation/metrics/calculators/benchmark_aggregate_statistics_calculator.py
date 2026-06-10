from __future__ import annotations

from collections.abc import Sequence
from statistics import mean, median, stdev

from src.evaluation.metrics.entities.experiment_result_snapshot import (
    ExperimentResultSnapshot,
)


class BenchmarkAggregateStatisticsCalculator:
    """
    Calculates aggregate statistics from experiment snapshots.
    """

    @staticmethod
    def calculate_scores(
        *,
        snapshots: Sequence[ExperimentResultSnapshot],
    ) -> tuple[float, ...]:
        return tuple(
            snapshot.overall_score
            for snapshot in snapshots
        )

    @staticmethod
    def calculate_mean(
        *,
        scores: tuple[float, ...],
    ) -> float:
        return mean(scores)

    @staticmethod
    def calculate_median(
        *,
        scores: tuple[float, ...],
    ) -> float:
        return median(scores)

    @staticmethod
    def calculate_min(
        *,
        scores: tuple[float, ...],
    ) -> float:
        return min(scores)

    @staticmethod
    def calculate_max(
        *,
        scores: tuple[float, ...],
    ) -> float:
        return max(scores)

    @staticmethod
    def calculate_standard_deviation(
        *,
        scores: tuple[float, ...],
    ) -> float:
        if len(scores) == 1:
            return 0.0

        return stdev(scores)

    @staticmethod
    def find_best_snapshot(
        *,
        snapshots: Sequence[ExperimentResultSnapshot],
    ) -> ExperimentResultSnapshot:
        return max(
            snapshots,
            key=lambda snapshot: snapshot.overall_score,
        )

    @staticmethod
    def find_worst_snapshot(
        *,
        snapshots: Sequence[ExperimentResultSnapshot],
    ) -> ExperimentResultSnapshot:
        return min(
            snapshots,
            key=lambda snapshot: snapshot.overall_score,
        )