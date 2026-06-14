from __future__ import annotations

from src.evaluation.tracking.entities.experiment_run import (
    ExperimentRun,
)
from src.evaluation.tracking.repositories.experiment_run_repository import (
    ExperimentRunRepository,
)
from src.evaluation.tracking.value_objects.experiment_query import (
    ExperimentQuery,
)


class ExperimentRunQueryLoader:
    """
    Loads experiment runs from repository according
    to the most selective query key.
    """

    def __init__(
        self,
        *,
        run_repository: ExperimentRunRepository,
    ) -> None:
        self._run_repository = run_repository

    def load(
        self,
        *,
        query: ExperimentQuery,
    ) -> tuple[
        ExperimentRun,
        ...,
    ]:
        if query.run_id is not None:
            run = self._run_repository.get_by_id(
                run_id=query.run_id,
            )

            return (
                ()
                if run is None
                else (run,)
            )

        if query.experiment_id is not None:
            return self._run_repository.list_by_experiment(
                experiment_id=query.experiment_id,
            )

        if query.status is not None:
            return self._run_repository.list_by_status(
                status=query.status,
            )

        return self._run_repository.list_all()