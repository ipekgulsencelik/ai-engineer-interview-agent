from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from src.evaluation.tracking.enums.worker_node_status import (
    WorkerNodeStatus,
)
from src.evaluation.tracking.validators.worker_node_validator import (
    WorkerNodeValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class WorkerNode:
    """
    Immutable worker node.

    Represents a distributed worker capable of
    executing evaluation, tracking, artifact,
    registry, and orchestration workloads.
    """

    node_id: str

    worker_id: str

    worker_name: str

    hostname: str

    region: str

    status: WorkerNodeStatus

    started_at: datetime

    last_heartbeat_at: datetime

    queue_name: str | None = None

    current_job_id: str | None = None

    processed_job_count: int = 0

    failed_job_count: int = 0

    max_concurrency: int = 1

    metadata: dict[
        str,
        str,
    ] | None = None

    notes: str | None = None

    def __post_init__(
        self,
    ) -> None:
        WorkerNodeValidator.validate(
            node_id=self.node_id,
            worker_id=self.worker_id,
            worker_name=self.worker_name,
            hostname=self.hostname,
            region=self.region,
            status=self.status,
            started_at=self.started_at,
            last_heartbeat_at=self.last_heartbeat_at,
            queue_name=self.queue_name,
            current_job_id=self.current_job_id,
            processed_job_count=self.processed_job_count,
            failed_job_count=self.failed_job_count,
            max_concurrency=self.max_concurrency,
            metadata=self.metadata,
            notes=self.notes,
        )

    @property
    def active(
        self,
    ) -> bool:
        return (
            self.status
            == WorkerNodeStatus.ACTIVE
        )

    @property
    def is_idle(
        self,
    ) -> bool:
        return (
            self.current_job_id
            is None
        )

    @property
    def is_busy(
        self,
    ) -> bool:
        return (
            self.current_job_id
            is not None
        )

    @property
    def is_offline(
        self,
    ) -> bool:
        return (
            self.status
            == WorkerNodeStatus.OFFLINE
        )

    @property
    def is_draining(
        self,
    ) -> bool:
        return (
            self.status
            == WorkerNodeStatus.DRAINING
        )

    @property
    def is_failed(
        self,
    ) -> bool:
        return (
            self.status
            == WorkerNodeStatus.FAILED
        )

    @property
    def has_failures(
        self,
    ) -> bool:
        return (
            self.failed_job_count > 0
        )

    @property
    def success_rate(
        self,
    ) -> float:
        total = (
            self.processed_job_count
            + self.failed_job_count
        )

        if total == 0:
            return 1.0

        return (
            self.processed_job_count
            / total
        )

    @property
    def has_metadata(
        self,
    ) -> bool:
        return bool(
            self.metadata,
        )