from __future__ import annotations

from datetime import datetime

from src.evaluation.tracking.entities.worker_node import (
    WorkerNode,
)
from src.evaluation.tracking.factories.worker_tracking_event_factory import (
    WorkerTrackingEventFactory,
)
from src.evaluation.tracking.publishers.tracking_event_publisher import (
    TrackingEventPublisher,
)
from src.evaluation.tracking.queues.async_event_queue import (
    AsyncEventQueue,
)
from src.evaluation.tracking.registries.worker_node_registry import (
    WorkerNodeRegistry,
)
from src.evaluation.tracking.services.worker_job_service import (
    WorkerJobService,
)
from src.evaluation.tracking.services.worker_lifecycle_service import (
    WorkerLifecycleService,
)
from src.evaluation.tracking.validators.worker_node_validator import (
    WorkerNodeValidator,
)


class DistributedTrackingCoordinator:
    """
    Coordinates distributed worker tracking.
    """

    def __init__(
        self,
        *,
        event_queue: AsyncEventQueue,
        registry: WorkerNodeRegistry | None = None,
        lifecycle_service: WorkerLifecycleService | None = None,
        job_service: WorkerJobService | None = None,
    ) -> None:
        self._registry = (
            registry
            or WorkerNodeRegistry()
        )

        event_factory = WorkerTrackingEventFactory()

        event_publisher = TrackingEventPublisher(
            event_queue=event_queue,
        )

        validator = WorkerNodeValidator()

        self._lifecycle_service = (
            lifecycle_service
            or WorkerLifecycleService(
                registry=self._registry,
                event_factory=event_factory,
                event_publisher=event_publisher,
                validator=validator,
            )
        )

        self._job_service = (
            job_service
            or WorkerJobService(
                registry=self._registry,
                event_factory=event_factory,
                event_publisher=event_publisher,
                validator=validator,
            )
        )

    async def register_worker(
        self,
        *,
        worker: WorkerNode,
    ) -> WorkerNode:
        return await self._lifecycle_service.register_worker(
            worker=worker,
        )

    async def heartbeat(
        self,
        *,
        node_id: str,
        occurred_at: datetime | None = None,
    ) -> WorkerNode:
        return await self._lifecycle_service.heartbeat(
            node_id=node_id,
            occurred_at=occurred_at,
        )

    async def assign_job(
        self,
        *,
        node_id: str,
        job_id: str,
    ) -> WorkerNode:
        return await self._job_service.assign_job(
            node_id=node_id,
            job_id=job_id,
        )

    async def complete_job(
        self,
        *,
        node_id: str,
        job_id: str,
    ) -> WorkerNode:
        return await self._job_service.complete_job(
            node_id=node_id,
            job_id=job_id,
        )

    async def fail_job(
        self,
        *,
        node_id: str,
        job_id: str,
        error_message: str | None = None,
    ) -> WorkerNode:
        return await self._job_service.fail_job(
            node_id=node_id,
            job_id=job_id,
            error_message=error_message,
        )

    async def mark_draining(
        self,
        *,
        node_id: str,
    ) -> WorkerNode:
        return await self._lifecycle_service.mark_draining(
            node_id=node_id,
        )

    async def mark_offline(
        self,
        *,
        node_id: str,
    ) -> WorkerNode:
        return await self._lifecycle_service.mark_offline(
            node_id=node_id,
        )

    async def mark_failed(
        self,
        *,
        node_id: str,
        error_message: str | None = None,
    ) -> WorkerNode:
        return await self._lifecycle_service.mark_failed(
            node_id=node_id,
            error_message=error_message,
        )

    def get_worker(
        self,
        *,
        node_id: str,
    ) -> WorkerNode | None:
        return self._registry.get(
            node_id=node_id,
        )

    def list_workers(
        self,
    ) -> tuple[
        WorkerNode,
        ...,
    ]:
        return self._registry.list_all()

    def list_active_workers(
        self,
    ) -> tuple[
        WorkerNode,
        ...,
    ]:
        return self._registry.list_active()