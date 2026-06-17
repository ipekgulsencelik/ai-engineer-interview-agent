from __future__ import annotations

from collections import deque
from collections.abc import Iterator
from threading import Lock

from src.evaluation.reporting.entities.stream_event import (
    StreamEvent,
)


class StreamEventStore:
    """
    Thread-safe in-memory event store for stream events.
    """

    def __init__(
        self,
        *,
        max_events: int = 10_000,
    ) -> None:
        self._events: deque[
            StreamEvent
        ] = deque(
            maxlen=max_events,
        )

        self._lock = Lock()

    def append(
        self,
        *,
        event: StreamEvent,
    ) -> None:
        with self._lock:
            self._events.append(
                event,
            )

    def latest(
        self,
        *,
        limit: int = 100,
    ) -> tuple[
        StreamEvent,
        ...,
    ]:
        with self._lock:
            return tuple(
                list(
                    self._events,
                )[-limit:]
            )

    def snapshot(
        self,
    ) -> tuple[
        StreamEvent,
        ...,
    ]:
        with self._lock:
            return tuple(
                self._events,
            )

    def clear(
        self,
    ) -> None:
        with self._lock:
            self._events.clear()

    def contains(
        self,
        *,
        event_id: str,
    ) -> bool:
        with self._lock:
            return any(
                event.event_id == event_id
                for event in self._events
            )

    def stream(
        self,
    ) -> Iterator[
        StreamEvent
    ]:
        yield from self.snapshot()

    @property
    def count(
        self,
    ) -> int:
        with self._lock:
            return len(
                self._events,
            )

    @property
    def is_empty(
        self,
    ) -> bool:
        return self.count == 0