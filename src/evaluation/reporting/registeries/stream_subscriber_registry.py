from __future__ import annotations

from collections.abc import Callable
from threading import Lock

from src.evaluation.reporting.entities.stream_event import (
    StreamEvent,
)


class StreamSubscriberRegistry:
    """
    Thread-safe registry for stream subscribers.
    """

    def __init__(
        self,
    ) -> None:
        self._subscribers: dict[
            str,
            Callable[
                [StreamEvent],
                None,
            ],
        ] = {}

        self._lock = Lock()

    def subscribe(
        self,
        *,
        subscriber_id: str,
        callback: Callable[
            [StreamEvent],
            None,
        ],
    ) -> None:
        with self._lock:
            self._subscribers[
                subscriber_id
            ] = callback

    def unsubscribe(
        self,
        *,
        subscriber_id: str,
    ) -> None:
        with self._lock:
            self._subscribers.pop(
                subscriber_id,
                None,
            )

    def notify(
        self,
        *,
        event: StreamEvent,
    ) -> None:
        for subscriber in self.snapshot():
            subscriber(
                event,
            )

    def snapshot(
        self,
    ) -> tuple[
        Callable[
            [StreamEvent],
            None,
        ],
        ...,
    ]:
        with self._lock:
            return tuple(
                self._subscribers.values(),
            )

    @property
    def count(
        self,
    ) -> int:
        with self._lock:
            return len(
                self._subscribers,
            )