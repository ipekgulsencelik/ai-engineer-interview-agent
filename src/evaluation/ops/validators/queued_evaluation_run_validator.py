from __future__ import annotations

from datetime import datetime

from src.domain.validation.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.ops.enums.evaluation_queue_status import (
    EvaluationQueueStatus,
)
from src.evaluation.ops.schemas.queued_evaluation_run_schema import (
    QUEUED_EVALUATION_RUN_SCHEMA,
)


class QueuedEvaluationRunValidator:
    """
    QueuedEvaluationRun validation service.
    """

    @staticmethod
    def validate(
        *,
        queue_id: str,
        run_id: str,
        benchmark_id: str,
        benchmark_name: str,
        benchmark_version: str,
        experiment_id: str,
        model_name: str,
        priority: int,
        status: EvaluationQueueStatus,
        requested_by: str,
        queued_at: datetime,
        scheduled_at: datetime | None,
        notes: str | None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "queue_id": queue_id,
                "run_id": run_id,
                "benchmark_id": benchmark_id,
                "benchmark_name": benchmark_name,
                "benchmark_version": benchmark_version,
                "experiment_id": experiment_id,
                "model_name": model_name,
                "priority": priority,
                "requested_by": requested_by,
                "queued_at": queued_at,
                "scheduled_at": scheduled_at,
                "notes": notes,
            },
            schema=QUEUED_EVALUATION_RUN_SCHEMA,
            error_factory=EvaluationValidationError,
        )

        if not isinstance(
            status,
            EvaluationQueueStatus,
        ):
            raise EvaluationValidationError(
                "status must be EvaluationQueueStatus."
            )

        if (
            status == EvaluationQueueStatus.SCHEDULED
            and scheduled_at is None
        ):
            raise EvaluationValidationError(
                "scheduled_at is required for scheduled runs."
            )

        if (
            status == EvaluationQueueStatus.QUEUED
            and scheduled_at is not None
        ):
            raise EvaluationValidationError(
                "scheduled_at must be None for queued runs."
            )

        if (
            scheduled_at is not None
            and scheduled_at < queued_at
        ):
            raise EvaluationValidationError(
                "scheduled_at cannot be earlier than queued_at."
            )