from __future__ import annotations

from src.evaluation.tracking.entities.experiment_run import (
    ExperimentRun,
)


class ExperimentWinnerSelector:
    """
    Selects the winning experiment based on
    comparison metrics.
    """

    @staticmethod
    def select(
        *,
        baseline: ExperimentRun,
        candidate: ExperimentRun,
    ) -> str | None:
        if (
            baseline.overall_score is None
            or candidate.overall_score is None
        ):
            return None

        if (
            candidate.overall_score
            > baseline.overall_score
        ):
            return candidate.experiment_id

        if (
            baseline.overall_score
            > candidate.overall_score
        ):
            return baseline.experiment_id

        return None