from __future__ import annotations

from src.evaluation.tracking.entities.tracking_event import (
    TrackingEvent,
)
from src.evaluation.tracking.registries.event_handler_registry import (
    EventHandlerRegistry,
)


class TrackingEventDispatcher:
    """
    Dispatches tracking events to registered handlers.
    """

    def __init__(
        self,
        *,
        handler_registry: EventHandlerRegistry,
    ) -> None:
        self._handler_registry = handler_registry

    async def dispatch(
        self,
        *,
        event: TrackingEvent,
    ) -> None:
        for handler in self._handler_registry.list_handlers():
            await handler(
                event,
            )