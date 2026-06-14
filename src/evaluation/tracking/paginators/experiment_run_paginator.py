from __future__ import annotations

from src.evaluation.tracking.entities.experiment_run import (
    ExperimentRun,
)
from src.evaluation.tracking.value_objects.experiment_query import (
    ExperimentQuery,
)


class ExperimentRunPaginator:
    """
    Applies offset-limit pagination to experiment runs.
    """

    @staticmethod
    def paginate(
        *,
        runs: tuple[
            ExperimentRun,
            ...,
        ],
        query: ExperimentQuery,
    ) -> tuple[
        ExperimentRun,
        ...,
    ]:
        start = query.offset or 0

        if query.limit is None:
            return runs[
                start:
            ]

        return runs[
            start : start + query.limit
        ]