from __future__ import annotations

from src.evaluation.reporting.entities.stream_event import (
    StreamEvent,
)
from src.evaluation.reporting.stores.stream_event_store import (
    StreamEventStore,
)


class StreamEventQueryService:
    """
    Query service for stream events.
    """

    def __init__(
        self,
        *,
        event_store: StreamEventStore,
    ) -> None:
        self._event_store = event_store

    def by_stream(
        self,
        *,
        stream_id: str,
    ) -> tuple[
        StreamEvent,
        ...,
    ]:
        return tuple(
            event
            for event in self._event_store.snapshot()
            if event.stream_id == stream_id
        )

    def by_type(
        self,
        *,
        event_type: str,
    ) -> tuple[
        StreamEvent,
        ...,
    ]:
        return tuple(
            event
            for event in self._event_store.snapshot()
            if event.event_type == event_type
        )

    def by_experiment(
        self,
        *,
        experiment_id: str,
    ) -> tuple[
        StreamEvent,
        ...,
    ]:
        return tuple(
            event
            for event in self._event_store.snapshot()
            if event.experiment_id == experiment_id
        )

    def by_run(
        self,
        *,
        run_id: str,
    ) -> tuple[
        StreamEvent,
        ...,
    ]:
        return tuple(
            event
            for event in self._event_store.snapshot()
            if event.run_id == run_id
        )

    def by_correlation(
        self,
        *,
        correlation_id: str,
    ) -> tuple[
        StreamEvent,
        ...,
    ]:
        return tuple(
            event
            for event in self._event_store.snapshot()
            if event.correlation_id == correlation_id
        )