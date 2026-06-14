from __future__ import annotations

from src.evaluation.tracking.filters.experiment_run_query_filter import (
    ExperimentRunQueryFilter,
)
from src.evaluation.tracking.loaders.experiment_run_query_loader import (
    ExperimentRunQueryLoader,
)
from src.evaluation.tracking.paginators.experiment_run_paginator import (
    ExperimentRunPaginator,
)
from src.evaluation.tracking.repositories.experiment_run_repository import (
    ExperimentRunRepository,
)
from src.evaluation.tracking.sorters.experiment_run_sorter import (
    ExperimentRunSorter,
)
from src.evaluation.tracking.value_objects.experiment_query import (
    ExperimentQuery,
)
from src.evaluation.tracking.entities.experiment_run import (
    ExperimentRun,
)


class ExperimentQueryEngine:
    """
    Application service for querying experiment runs.
    """

    def __init__(
        self,
        *,
        run_repository: ExperimentRunRepository,
        query_loader: ExperimentRunQueryLoader | None = None,
        query_filter: ExperimentRunQueryFilter | None = None,
        sorter: ExperimentRunSorter | None = None,
        paginator: ExperimentRunPaginator | None = None,
    ) -> None:
        self._query_loader = (
            query_loader
            or ExperimentRunQueryLoader(
                run_repository=run_repository,
            )
        )
        self._query_filter = (
            query_filter
            or ExperimentRunQueryFilter()
        )
        self._sorter = (
            sorter
            or ExperimentRunSorter()
        )
        self._paginator = (
            paginator
            or ExperimentRunPaginator()
        )

    def search(
        self,
        *,
        query: ExperimentQuery,
    ) -> tuple[
        ExperimentRun,
        ...,
    ]:
        runs = self._query_loader.load(
            query=query,
        )

        filtered_runs = self._query_filter.apply(
            runs=runs,
            query=query,
        )

        sorted_runs = self._sorter.sort_by_started_at_desc(
            runs=filtered_runs,
        )

        return self._paginator.paginate(
            runs=sorted_runs,
            query=query,
        )