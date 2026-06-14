from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from src.evaluation.tracking.entities.experiment_run import (
    ExperimentRun,
)
from src.evaluation.tracking.enums.experiment_run_status import (
    ExperimentRunStatus,
)


class ExperimentRunRepository(
    ABC,
):
    """
    Repository port for experiment run persistence.

    Infrastructure adapters should implement this
    interface for database, file, or external storage.
    """

    @abstractmethod
    def save(
        self,
        *,
        run: ExperimentRun,
    ) -> None:
        """
        Persists a new experiment run.
        """

    @abstractmethod
    def update(
        self,
        *,
        run: ExperimentRun,
    ) -> None:
        """
        Updates an existing experiment run.
        """

    @abstractmethod
    def get_by_id(
        self,
        *,
        run_id: str,
    ) -> ExperimentRun | None:
        """
        Returns an experiment run by id.
        """

    @abstractmethod
    def list_all(
        self,
    ) -> tuple[
        ExperimentRun,
        ...,
    ]:
        """
        Lists all experiment runs.
        """

    @abstractmethod
    def list_by_experiment(
        self,
        *,
        experiment_id: str,
    ) -> tuple[
        ExperimentRun,
        ...,
    ]:
        """
        Lists runs for one experiment.
        """

    @abstractmethod
    def list_by_status(
        self,
        *,
        status: ExperimentRunStatus,
    ) -> tuple[
        ExperimentRun,
        ...,
    ]:
        """
        Lists runs by lifecycle status.
        """

    @abstractmethod
    def exists(
        self,
        *,
        run_id: str,
    ) -> bool:
        """
        Returns whether a run exists.
        """