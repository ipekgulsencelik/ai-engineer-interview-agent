from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from src.evaluation.tracking.entities.experiment_run import (
    ExperimentRun,
)


class ExperimentRunStore(
    ABC,
):
    """
    Store port for experiment run persistence.
    """

    @abstractmethod
    def save_run(
        self,
        *,
        run: ExperimentRun,
    ) -> None:
        """
        Persists an experiment run snapshot.
        """

    @abstractmethod
    def get_run(
        self,
        *,
        run_id: str,
    ) -> ExperimentRun | None:
        """
        Returns a run by id.
        """

    @abstractmethod
    def list_runs(
        self,
        *,
        experiment_id: str,
    ) -> tuple[
        ExperimentRun,
        ...,
    ]:
        """
        Lists runs for a given experiment.
        """

    @abstractmethod
    def exists_run(
        self,
        *,
        run_id: str,
    ) -> bool:
        """
        Returns whether a run exists.
        """