from __future__ import annotations

from dataclasses import replace

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


class WorkerJobService:
    """
    Handles worker job assignment and completion.
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

    async def assign_job(
        self,
        *,
        node_id: str,
        job_id: str,
    ) -> WorkerNode:
        worker = self._validator.require_registered(
            registry=self._registry,
            node_id=node_id,
        )

        self._validator.ensure_can_receive_job(
            worker=worker,
        )

        updated_worker = replace(
            worker,
            current_job_id=job_id,
            status=WorkerNodeStatus.ACTIVE,
        )

        self._registry.update(
            worker=updated_worker,
        )

        await self._publish(
            event_type="worker_job_assigned",
            worker=updated_worker,
            payload={
                "job_id": job_id,
            },
        )

        return updated_worker

    async def complete_job(
        self,
        *,
        node_id: str,
        job_id: str,
    ) -> WorkerNode:
        worker = self._validator.require_registered(
            registry=self._registry,
            node_id=node_id,
        )

        self._validator.ensure_current_job(
            worker=worker,
            job_id=job_id,
        )

        updated_worker = replace(
            worker,
            current_job_id=None,
            processed_job_count=(
                worker.processed_job_count + 1
            ),
            status=WorkerNodeStatus.IDLE,
        )

        self._registry.update(
            worker=updated_worker,
        )

        await self._publish(
            event_type="worker_job_completed",
            worker=updated_worker,
            payload={
                "job_id": job_id,
                "processed_job_count": (
                    updated_worker.processed_job_count
                ),
            },
        )

        return updated_worker

    async def fail_job(
        self,
        *,
        node_id: str,
        job_id: str,
        error_message: str | None = None,
    ) -> WorkerNode:
        worker = self._validator.require_registered(
            registry=self._registry,
            node_id=node_id,
        )

        self._validator.ensure_current_job(
            worker=worker,
            job_id=job_id,
        )

        updated_worker = replace(
            worker,
            current_job_id=None,
            failed_job_count=(
                worker.failed_job_count + 1
            ),
            status=WorkerNodeStatus.IDLE,
        )

        self._registry.update(
            worker=updated_worker,
        )

        await self._publish(
            event_type="worker_job_failed",
            worker=updated_worker,
            payload={
                "job_id": job_id,
                "failed_job_count": (
                    updated_worker.failed_job_count
                ),
                "error_message": error_message,
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
    ) -> None:
        event = self._event_factory.create(
            event_type=event_type,
            worker=worker,
            payload=payload,
        )

        await self._event_publisher.publish(
            event=event,
        )