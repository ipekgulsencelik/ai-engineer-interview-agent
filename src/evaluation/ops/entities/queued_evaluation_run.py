from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from src.evaluation.ops.enums.evaluation_queue_status import (
    EvaluationQueueStatus,
)
from src.evaluation.ops.validators.queued_evaluation_run_validator import (
    QueuedEvaluationRunValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class QueuedEvaluationRun:
    """
    Immutable queued evaluation run.

    Represents an evaluation request waiting
    to be executed by an evaluation worker.
    """

    queue_id: str

    run_id: str

    benchmark_id: str
    benchmark_name: str
    benchmark_version: str

    experiment_id: str

    model_name: str

    priority: int

    status: EvaluationQueueStatus

    requested_by: str

    queued_at: datetime

    scheduled_at: datetime | None = None

    notes: str | None = None

    def __post_init__(
        self,
    ) -> None:
        QueuedEvaluationRunValidator.validate(
            queue_id=self.queue_id,
            run_id=self.run_id,
            benchmark_id=self.benchmark_id,
            benchmark_name=self.benchmark_name,
            benchmark_version=self.benchmark_version,
            experiment_id=self.experiment_id,
            model_name=self.model_name,
            priority=self.priority,
            status=self.status,
            requested_by=self.requested_by,
            queued_at=self.queued_at,
            scheduled_at=self.scheduled_at,
            notes=self.notes,
        )

    @property
    def is_queued(
        self,
    ) -> bool:
        return (
            self.status
            == EvaluationQueueStatus.QUEUED
        )

    @property
    def is_scheduled(
        self,
    ) -> bool:
        return (
            self.status
            == EvaluationQueueStatus.SCHEDULED
        )

    @property
    def waiting_for_execution(
        self,
    ) -> bool:
        return self.status in {
            EvaluationQueueStatus.QUEUED,
            EvaluationQueueStatus.SCHEDULED,
        }