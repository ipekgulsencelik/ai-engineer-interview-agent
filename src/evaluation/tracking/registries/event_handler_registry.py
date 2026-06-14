from __future__ import annotations

from collections.abc import Awaitable
from collections.abc import Callable

from src.evaluation.tracking.entities.tracking_event import (
    TrackingEvent,
)


EventHandler = Callable[
    [TrackingEvent],
    Awaitable[None],
]


class EventHandlerRegistry:
    """
    Registry for async tracking event handlers.
    """

    def __init__(
        self,
    ) -> None:
        self._handlers: list[
            EventHandler
        ] = []

    def register(
        self,
        *,
        handler: EventHandler,
    ) -> None:
        self._handlers.append(
            handler,
        )

    def list_handlers(
        self,
    ) -> tuple[
        EventHandler,
        ...,
    ]:
        return tuple(
            self._handlers,
        )

    @property
    def has_handlers(
        self,
    ) -> bool:
        return bool(
            self._handlers,
        )