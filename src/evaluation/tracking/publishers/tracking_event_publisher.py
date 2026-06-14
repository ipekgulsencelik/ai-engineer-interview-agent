from __future__ import annotations

from src.evaluation.tracking.entities.tracking_event import (
    TrackingEvent,
)
from src.evaluation.tracking.events.async_event_queue import (
    AsyncEventQueue,
)


class TrackingEventPublisher:
    """
    Publishes tracking events to the async event queue.
    """

    def __init__(
        self,
        *,
        event_queue: AsyncEventQueue,
    ) -> None:
        self._event_queue = event_queue

    async def publish(
        self,
        *,
        event: TrackingEvent,
    ) -> None:
        await self._event_queue.publish(
            event=event,
        )