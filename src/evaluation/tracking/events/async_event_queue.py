from __future__ import annotations

import asyncio

from src.evaluation.tracking.entities.tracking_event import (
    TrackingEvent,
)
from src.evaluation.tracking.events.event_handler import (
    EventHandler,
)
from src.evaluation.tracking.registries.event_handler_registry import (
    EventHandlerRegistry,
)
from src.evaluation.tracking.events.tracking_event_dispatcher import (
    TrackingEventDispatcher,
)


class AsyncEventQueue:
    """
    Async in-memory event queue.
    """

    def __init__(
        self,
        *,
        maxsize: int = 0,
        handler_registry: EventHandlerRegistry | None = None,
        dispatcher: TrackingEventDispatcher | None = None,
    ) -> None:
        self._queue: asyncio.Queue[
            TrackingEvent
        ] = asyncio.Queue(
            maxsize=maxsize,
        )

        self._handler_registry = (
            handler_registry
            or EventHandlerRegistry()
        )

        self._dispatcher = (
            dispatcher
            or TrackingEventDispatcher(
                handler_registry=self._handler_registry,
            )
        )

        self._running = False

    def register_handler(
        self,
        *,
        handler: EventHandler,
    ) -> None:
        self._handler_registry.register(
            handler=handler,
        )

    async def publish(
        self,
        *,
        event: TrackingEvent,
    ) -> None:
        await self._queue.put(
            event,
        )

    async def consume_once(
        self,
    ) -> None:
        event = await self._queue.get()

        try:
            await self._dispatcher.dispatch(
                event=event,
            )
        finally:
            self._queue.task_done()

    async def run_forever(
        self,
    ) -> None:
        self._running = True

        while self._running:
            await self.consume_once()

    def stop(
        self,
    ) -> None:
        self._running = False

    async def drain(
        self,
    ) -> None:
        await self._queue.join()

    @property
    def size(
        self,
    ) -> int:
        return self._queue.qsize()

    @property
    def has_handlers(
        self,
    ) -> bool:
        return self._handler_registry.has_handlers