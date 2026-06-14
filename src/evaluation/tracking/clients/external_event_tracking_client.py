from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from src.evaluation.tracking.entities.tracking_event import (
    TrackingEvent,
)


class ExternalEventTrackingClient(
    ABC,
):
    """
    Client port for external event tracking.
    """

    @abstractmethod
    async def log_event(
        self,
        *,
        event: TrackingEvent,
    ) -> None:
        """
        Sends a tracking event to the external system.
        """