from __future__ import annotations

from datetime import UTC
from datetime import datetime

from src.evaluation.tracking.entities.tracking_event import (
    TrackingEvent,
)
from src.evaluation.tracking.entities.worker_node import (
    WorkerNode,
)


class WorkerTrackingEventFactory:
    """
    Builds tracking events for worker node lifecycle.
    """

    @staticmethod
    def create(
        *,
        event_type: str,
        worker: WorkerNode,
        payload: dict[
            str,
            object,
        ],
        occurred_at: datetime | None = None,
    ) -> TrackingEvent:
        now = datetime.now(
            UTC,
        )

        return TrackingEvent(
            event_id=(
                f"{event_type}:"
                f"{worker.node_id}:"
                f"{now.timestamp()}"
            ),
            event_type=event_type,
            occurred_at=(
                occurred_at
                or now
            ),
            source="distributed_tracking_coordinator",
            entity_type="worker_node",
            entity_id=worker.node_id,
            payload=payload,
            actor=None,
            run_id=None,
            experiment_id=None,
            correlation_id=None,
            trace_id=None,
            description=None,
            metadata={
                "worker_id": worker.worker_id,
                "hostname": worker.hostname,
                "region": worker.region,
            },
        )