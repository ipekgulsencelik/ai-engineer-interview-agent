from __future__ import annotations

from datetime import UTC
from datetime import datetime
from uuid import uuid4

from src.evaluation.reporting.entities.stream_event import (
    StreamEvent,
)


class BenchmarkStreamEventFactory:
    """
    Factory for creating benchmark stream events.
    """

    ENTITY_TYPE = "benchmark"

    def create(
        self,
        *,
        event_type: str,
        result_id: str,
        sequence_number: int,
        payload: dict[str, str],
        runner_name: str,
        run_id: str,
        experiment_id: str,
        correlation_id: str | None = None,
        trace_id: str | None = None,
        metadata: dict[str, str] | None = None,
    ) -> StreamEvent:
        return StreamEvent(
            event_id=str(
                uuid4(),
            ),
            stream_id=result_id,
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
            entity_id=result_id,
            metadata=metadata,
        )