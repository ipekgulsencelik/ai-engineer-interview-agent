from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from src.evaluation.tracking.validators.tracking_event_validator import (
    TrackingEventValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class TrackingEvent:
    """
    Immutable tracking event.

    Represents an operational event emitted during
    experiment, model registry, artifact, lineage,
    benchmark, dataset, and evaluation lifecycle
    operations.
    """

    event_id: str

    event_type: str

    occurred_at: datetime

    source: str

    entity_type: str

    entity_id: str

    payload: dict[
        str,
        Any,
    ] | None = None

    actor: str | None = None

    run_id: str | None = None

    experiment_id: str | None = None

    correlation_id: str | None = None

    trace_id: str | None = None

    description: str | None = None

    metadata: dict[
        str,
        str,
    ] | None = None

    def __post_init__(
        self,
    ) -> None:
        TrackingEventValidator.validate(
            event_id=self.event_id,
            event_type=self.event_type,
            occurred_at=self.occurred_at,
            source=self.source,
            entity_type=self.entity_type,
            entity_id=self.entity_id,
            payload=self.payload,
            actor=self.actor,
            run_id=self.run_id,
            experiment_id=self.experiment_id,
            correlation_id=self.correlation_id,
            trace_id=self.trace_id,
            description=self.description,
            metadata=self.metadata,
        )

    @property
    def has_payload(
        self,
    ) -> bool:
        return bool(
            self.payload,
        )

    @property
    def has_actor(
        self,
    ) -> bool:
        return (
            self.actor
            is not None
        )

    @property
    def has_run(
        self,
    ) -> bool:
        return (
            self.run_id
            is not None
        )

    @property
    def has_experiment(
        self,
    ) -> bool:
        return (
            self.experiment_id
            is not None
        )

    @property
    def has_correlation(
        self,
    ) -> bool:
        return (
            self.correlation_id
            is not None
        )

    @property
    def has_trace(
        self,
    ) -> bool:
        return (
            self.trace_id
            is not None
        )

    @property
    def has_description(
        self,
    ) -> bool:
        return (
            self.description
            is not None
        )

    @property
    def has_metadata(
        self,
    ) -> bool:
        return bool(
            self.metadata,
        )