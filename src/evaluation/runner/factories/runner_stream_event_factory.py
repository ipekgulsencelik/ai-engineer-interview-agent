from __future__ import annotations

from datetime import UTC
from datetime import datetime
from uuid import uuid4

from src.evaluation.reporting.entities.stream_event import (
    StreamEvent,
)


class RunnerStreamEventFactory:
    """
    Factory for creating runner stream events.
    """

    ENTITY_TYPE = "runner"

    def create(
        self,
        *,
        event_type: str,
        execution_id: str,
        sequence_number: int,
        payload: dict[str, str],
        runner_id: str,
        runner_name: str,
        run_id: str | None = None,
        experiment_id: str | None = None,
        worker_id: str | None = None,
        correlation_id: str | None = None,
        trace_id: str | None = None,
        metadata: dict[str, str] | None = None,
    ) -> StreamEvent:
        return StreamEvent(
            event_id=str(
                uuid4(),
            ),
            stream_id=execution_id,
            event_type=event_type,
            occurred_at=datetime.now(
                UTC,
            ),
            source=runner_name,
            sequence_number=sequence_number,
            payload=payload,
            correlation_id=correlation_id,
            trace_id=trace_id,
            run_id=run_id,
            experiment_id=experiment_id,
            entity_type=self.ENTITY_TYPE,
            entity_id=runner_id,
            metadata={
                **(
                    metadata
                    or {}
                ),
                "worker_id": worker_id or "",
            },
        )