from __future__ import annotations

from src.evaluation.tracking.entities.experiment_node import (
    ExperimentNode,
)
from src.evaluation.tracking.value_objects.experiment_query import (
    ExperimentQuery,
)


class SQLiteExperimentPaginator:
    """
    Applies offset-limit pagination to experiment nodes.
    """

    @staticmethod
    def paginate(
        *,
        experiments: tuple[
            ExperimentNode,
            ...,
        ],
        query: ExperimentQuery,
    ) -> tuple[
        ExperimentNode,
        ...,
    ]:
        start = query.offset or 0

        if query.limit is None:
            return experiments[
                start:
            ]

        return experiments[
            start : start + query.limit
        ]