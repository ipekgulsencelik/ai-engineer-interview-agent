from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from src.evaluation.reporting.validators.stream_event_validator import (
    StreamEventValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class StreamEvent:
    """
    Immutable stream event.

    Represents a real-time event emitted during
    evaluation, experiment execution, dashboard
    updates, worker orchestration, artifact
    generation, or external tracking workflows.
    """

    event_id: str

    stream_id: str

    event_type: str

    occurred_at: datetime

    source: str

    sequence_number: int

    payload: dict[
        str,
        Any,
    ]

    correlation_id: str | None = None

    trace_id: str | None = None

    run_id: str | None = None

    experiment_id: str | None = None

    entity_type: str | None = None

    entity_id: str | None = None

    metadata: dict[
        str,
        str,
    ] | None = None

    def __post_init__(
        self,
    ) -> None:
        StreamEventValidator.validate(
            event_id=self.event_id,
            stream_id=self.stream_id,
            event_type=self.event_type,
            occurred_at=self.occurred_at,
            source=self.source,
            sequence_number=self.sequence_number,
            payload=self.payload,
            correlation_id=self.correlation_id,
            trace_id=self.trace_id,
            run_id=self.run_id,
            experiment_id=self.experiment_id,
            entity_type=self.entity_type,
            entity_id=self.entity_id,
            metadata=self.metadata,
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
    def has_entity(
        self,
    ) -> bool:
        return (
            self.entity_type is not None
            and self.entity_id is not None
        )

    @property
    def has_metadata(
        self,
    ) -> bool:
        return bool(
            self.metadata,
        )