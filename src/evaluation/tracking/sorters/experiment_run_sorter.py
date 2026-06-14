from __future__ import annotations

from src.evaluation.tracking.entities.experiment_run import (
    ExperimentRun,
)


class ExperimentRunSorter:
    """
    Sorts experiment runs.
    """

    @staticmethod
    def sort_by_started_at_desc(
        *,
        runs: tuple[
            ExperimentRun,
            ...,
        ],
    ) -> tuple[
        ExperimentRun,
        ...,
    ]:
        return tuple(
            sorted(
                runs,
                key=lambda run: run.started_at,
                reverse=True,
            )
        )