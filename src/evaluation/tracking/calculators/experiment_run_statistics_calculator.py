from __future__ import annotations

from src.evaluation.tracking.entities.experiment_run import (
    ExperimentRun,
)


class ExperimentRunStatisticsCalculator:
    """
    Calculates aggregate run statistics.
    """

    @staticmethod
    def average_score(
        *,
        runs: tuple[
            ExperimentRun,
            ...,
        ],
    ) -> float | None:
        scores = tuple(
            run.overall_score
            for run in runs
            if run.overall_score is not None
        )

        if not scores:
            return None

        return (
            sum(scores)
            / len(scores)
        )

    @staticmethod
    def best_run(
        *,
        runs: tuple[
            ExperimentRun,
            ...,
        ],
    ) -> ExperimentRun | None:
        if not runs:
            return None

        return max(
            runs,
            key=lambda run: (
                run.overall_score
                if run.overall_score is not None
                else -1.0
            ),
        )

    @staticmethod
    def worst_run(
        *,
        runs: tuple[
            ExperimentRun,
            ...,
        ],
    ) -> ExperimentRun | None:
        if not runs:
            return None

        return min(
            runs,
            key=lambda run: (
                run.overall_score
                if run.overall_score is not None
                else 1.0
            ),
        )