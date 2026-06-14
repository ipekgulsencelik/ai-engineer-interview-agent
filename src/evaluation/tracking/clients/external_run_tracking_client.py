from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from src.evaluation.tracking.entities.experiment_run import (
    ExperimentRun,
)


class ExternalRunTrackingClient(
    ABC,
):
    """
    Client port for external experiment run tracking.
    """

    @abstractmethod
    async def log_run(
        self,
        *,
        run: ExperimentRun,
    ) -> None:
        """
        Sends experiment run metadata to the external system.
        """

    @abstractmethod
    async def update_run(
        self,
        *,
        run: ExperimentRun,
    ) -> None:
        """
        Updates experiment run metadata in the external system.
        """