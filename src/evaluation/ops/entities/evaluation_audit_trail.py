from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from src.evaluation.ops.value_objects.audit_event import (
    AuditEvent,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class EvaluationAuditTrail:
    """
    Immutable evaluation audit trail.

    Represents an ordered collection of audit events
    produced during an evaluation lifecycle.
    """

    trail_id: str

    evaluation_run_id: str

    experiment_id: str
    benchmark_id: str

    events: tuple[
        AuditEvent,
        ...,
    ]

    created_at: datetime

    def __post_init__(
        self,
    ) -> None:
        EvaluationAuditTrailValidator.validate(
            trail_id=self.trail_id,
            evaluation_run_id=(
                self.evaluation_run_id
            ),
            experiment_id=self.experiment_id,
            benchmark_id=self.benchmark_id,
            events=self.events,
            created_at=self.created_at,
        )

    @property
    def event_count(
        self,
    ) -> int:
        return len(
            self.events,
        )

    @property
    def has_events(
        self,
    ) -> bool:
        return bool(
            self.events,
        )

    @property
    def first_event(
        self,
    ) -> AuditEvent | None:
        if not self.events:
            return None

        return self.events[0]

    @property
    def last_event(
        self,
    ) -> AuditEvent | None:
        if not self.events:
            return None

        return self.events[-1]

    @property
    def started_at(
        self,
    ) -> datetime | None:
        first_event = self.first_event

        if first_event is None:
            return None

        return first_event.occurred_at

    @property
    def latest_occurred_at(
        self,
    ) -> datetime | None:
        last_event = self.last_event

        if last_event is None:
            return None

        return last_event.occurred_at

    def contains_event_type(
        self,
        event_type: object,
    ) -> bool:
        return any(
            event.event_type == event_type
            for event in self.events
        )

    def events_for_aggregate(
        self,
        aggregate_id: str,
    ) -> tuple[
        AuditEvent,
        ...,
    ]:
        return tuple(
            event
            for event in self.events
            if event.aggregate_id == aggregate_id
        )