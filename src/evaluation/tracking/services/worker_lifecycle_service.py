from __future__ import annotations

from dataclasses import replace
from datetime import UTC
from datetime import datetime

from src.evaluation.tracking.entities.worker_node import (
    WorkerNode,
)
from src.evaluation.tracking.enums.worker_node_status import (
    WorkerNodeStatus,
)
from src.evaluation.tracking.factories.worker_tracking_event_factory import (
    WorkerTrackingEventFactory,
)
from src.evaluation.tracking.publishers.tracking_event_publisher import (
    TrackingEventPublisher,
)
from src.evaluation.tracking.registries.worker_node_registry import (
    WorkerNodeRegistry,
)
from src.evaluation.tracking.validators.worker_node_validator import (
    WorkerNodeValidator,
)


class WorkerLifecycleService:
    """
    Handles worker lifecycle state transitions.
    """

    def __init__(
        self,
        *,
        registry: WorkerNodeRegistry,
        event_factory: WorkerTrackingEventFactory,
        event_publisher: TrackingEventPublisher,
        validator: WorkerNodeValidator | None = None,
    ) -> None:
        self._registry = registry
        self._event_factory = event_factory
        self._event_publisher = event_publisher
        self._validator = (
            validator
            or WorkerNodeValidator()
        )

    async def register_worker(
        self,
        *,
        worker: WorkerNode,
    ) -> WorkerNode:
        self._validator.ensure_not_registered(
            registry=self._registry,
            node_id=worker.node_id,
        )

        self._registry.add(
            worker=worker,
        )

        await self._publish(
            event_type="worker_registered",
            worker=worker,
            payload={
                "worker_id": worker.worker_id,
                "worker_name": worker.worker_name,
                "hostname": worker.hostname,
                "region": worker.region,
                "status": str(
                    worker.status,
                ),
            },
        )

        return worker

    async def heartbeat(
        self,
        *,
        node_id: str,
        occurred_at: datetime | None = None,
    ) -> WorkerNode:
        worker = self._validator.require_registered(
            registry=self._registry,
            node_id=node_id,
        )

        heartbeat_at = (
            occurred_at
            or datetime.now(
                UTC,
            )
        )

        updated_worker = replace(
            worker,
            last_heartbeat_at=heartbeat_at,
        )

        self._registry.update(
            worker=updated_worker,
        )

        await self._publish(
            event_type="worker_heartbeat",
            worker=updated_worker,
            occurred_at=heartbeat_at,
            payload={
                "last_heartbeat_at": (
                    heartbeat_at.isoformat()
                ),
            },
        )

        return updated_worker

    async def mark_draining(
        self,
        *,
        node_id: str,
    ) -> WorkerNode:
        return await self._mark_status(
            node_id=node_id,
            status=WorkerNodeStatus.DRAINING,
            event_type="worker_draining",
            clear_job=False,
        )

    async def mark_offline(
        self,
        *,
        node_id: str,
    ) -> WorkerNode:
        return await self._mark_status(
            node_id=node_id,
            status=WorkerNodeStatus.OFFLINE,
            event_type="worker_offline",
            clear_job=True,
        )

    async def mark_failed(
        self,
        *,
        node_id: str,
        error_message: str | None = None,
    ) -> WorkerNode:
        worker = self._validator.require_registered(
            registry=self._registry,
            node_id=node_id,
        )

        updated_worker = replace(
            worker,
            status=WorkerNodeStatus.FAILED,
            current_job_id=None,
        )

        self._registry.update(
            worker=updated_worker,
        )

        await self._publish(
            event_type="worker_failed",
            worker=updated_worker,
            payload={
                "status": str(
                    updated_worker.status,
                ),
                "error_message": error_message,
            },
        )

        return updated_worker

    async def _mark_status(
        self,
        *,
        node_id: str,
        status: WorkerNodeStatus,
        event_type: str,
        clear_job: bool,
    ) -> WorkerNode:
        worker = self._validator.require_registered(
            registry=self._registry,
            node_id=node_id,
        )

        updated_worker = replace(
            worker,
            status=status,
            current_job_id=(
                None
                if clear_job
                else worker.current_job_id
            ),
        )

        self._registry.update(
            worker=updated_worker,
        )

        await self._publish(
            event_type=event_type,
            worker=updated_worker,
            payload={
                "status": str(
                    updated_worker.status,
                ),
            },
        )

        return updated_worker

    async def _publish(
        self,
        *,
        event_type: str,
        worker: WorkerNode,
        payload: dict[
            str,
            object,
        ],
        occurred_at: datetime | None = None,
    ) -> None:
        event = self._event_factory.create(
            event_type=event_type,
            worker=worker,
            payload=payload,
            occurred_at=occurred_at,
        )

        await self._event_publisher.publish(
            event=event,
        )