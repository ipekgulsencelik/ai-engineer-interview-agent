from __future__ import annotations

from collections.abc import Callable
from collections.abc import Iterator

from src.evaluation.reporting.entities.stream_event import (
    StreamEvent,
)
from src.evaluation.reporting.services.stream_event_query_service import (
    StreamEventQueryService,
)
from src.evaluation.reporting.stores.stream_event_store import (
    StreamEventStore,
)
from src.evaluation.reporting.registeries.stream_subscriber_registry import (
    StreamSubscriberRegistry,
)


class RealtimeAnalyticsStream:
    """
    Facade for real-time analytics stream operations.
    """

    def __init__(
        self,
        *,
        event_store: StreamEventStore | None = None,
        subscriber_registry: StreamSubscriberRegistry | None = None,
        query_service: StreamEventQueryService | None = None,
        max_events: int = 10_000,
    ) -> None:
        self._event_store = (
            event_store
            or StreamEventStore(
                max_events=max_events,
            )
        )

        self._subscriber_registry = (
            subscriber_registry
            or StreamSubscriberRegistry()
        )

        self._query_service = (
            query_service
            or StreamEventQueryService(
                event_store=self._event_store,
            )
        )

    def publish(
        self,
        *,
        event: StreamEvent,
    ) -> None:
        self._event_store.append(
            event=event,
        )

        self._subscriber_registry.notify(
            event=event,
        )

    def subscribe(
        self,
        *,
        subscriber_id: str,
        callback: Callable[
            [StreamEvent],
            None,
        ],
    ) -> None:
        self._subscriber_registry.subscribe(
            subscriber_id=subscriber_id,
            callback=callback,
        )

    def unsubscribe(
        self,
        *,
        subscriber_id: str,
    ) -> None:
        self._subscriber_registry.unsubscribe(
            subscriber_id=subscriber_id,
        )

    def latest_events(
        self,
        *,
        limit: int = 100,
    ) -> tuple[
        StreamEvent,
        ...,
    ]:
        return self._event_store.latest(
            limit=limit,
        )

    def events_by_stream(
        self,
        *,
        stream_id: str,
    ) -> tuple[
        StreamEvent,
        ...,
    ]:
        return self._query_service.by_stream(
            stream_id=stream_id,
        )

    def events_by_type(
        self,
        *,
        event_type: str,
    ) -> tuple[
        StreamEvent,
        ...,
    ]:
        return self._query_service.by_type(
            event_type=event_type,
        )

    def events_by_experiment(
        self,
        *,
        experiment_id: str,
    ) -> tuple[
        StreamEvent,
        ...,
    ]:
        return self._query_service.by_experiment(
            experiment_id=experiment_id,
        )

    def events_by_run(
        self,
        *,
        run_id: str,
    ) -> tuple[
        StreamEvent,
        ...,
    ]:
        return self._query_service.by_run(
            run_id=run_id,
        )

    def events_by_correlation(
        self,
        *,
        correlation_id: str,
    ) -> tuple[
        StreamEvent,
        ...,
    ]:
        return self._query_service.by_correlation(
            correlation_id=correlation_id,
        )

    def clear(
        self,
    ) -> None:
        self._event_store.clear()

    def contains(
        self,
        *,
        event_id: str,
    ) -> bool:
        return self._event_store.contains(
            event_id=event_id,
        )

    def stream(
        self,
    ) -> Iterator[
        StreamEvent
    ]:
        return self._event_store.stream()

    @property
    def event_count(
        self,
    ) -> int:
        return self._event_store.count

    @property
    def subscriber_count(
        self,
    ) -> int:
        return self._subscriber_registry.count

    @property
    def is_empty(
        self,
    ) -> bool:
        return self._event_store.is_empty