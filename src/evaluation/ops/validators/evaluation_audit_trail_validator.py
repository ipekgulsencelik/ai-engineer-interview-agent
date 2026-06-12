from __future__ import annotations

from datetime import datetime

from src.domain.validation.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.ops.constants.evaluation_audit_trail import (
    AUDIT_TRAIL_EMPTY_EVENTS_ERROR,
    AUDIT_TRAIL_EVENT_BENCHMARK_MISMATCH_ERROR,
    AUDIT_TRAIL_EVENT_EXPERIMENT_MISMATCH_ERROR,
    AUDIT_TRAIL_EVENT_ORDER_ERROR,
    AUDIT_TRAIL_EVENTS_TYPE_ERROR,
    AUDIT_TRAIL_EVENT_TYPE_ERROR,
)
from src.evaluation.ops.schemas.evaluation_audit_trail_schema import (
    EVALUATION_AUDIT_TRAIL_SCHEMA,
)
from src.evaluation.ops.value_objects.audit_event import (
    AuditEvent,
)


class EvaluationAuditTrailValidator:
    """
    EvaluationAuditTrail validation service.
    """

    @staticmethod
    def validate(
        *,
        trail_id: str,
        evaluation_run_id: str,
        experiment_id: str,
        benchmark_id: str,
        events: tuple[
            AuditEvent,
            ...,
        ],
        created_at: datetime,
    ) -> None:
        SchemaValidator.validate(
            values={
                "trail_id": trail_id,
                "evaluation_run_id": (
                    evaluation_run_id
                ),
                "experiment_id": experiment_id,
                "benchmark_id": benchmark_id,
                "created_at": created_at,
            },
            schema=(
                EVALUATION_AUDIT_TRAIL_SCHEMA
            ),
            error_factory=(
                EvaluationValidationError
            ),
        )

        if not isinstance(
            events,
            tuple,
        ):
            raise EvaluationValidationError(
                AUDIT_TRAIL_EVENTS_TYPE_ERROR
            )

        if not events:
            raise EvaluationValidationError(
                AUDIT_TRAIL_EMPTY_EVENTS_ERROR
            )

        previous_occurred_at: datetime | None = None

        for event in events:
            if not isinstance(
                event,
                AuditEvent,
            ):
                raise EvaluationValidationError(
                    AUDIT_TRAIL_EVENT_TYPE_ERROR
                )

            if event.experiment_id != experiment_id:
                raise EvaluationValidationError(
                    AUDIT_TRAIL_EVENT_EXPERIMENT_MISMATCH_ERROR
                )

            if event.benchmark_id != benchmark_id:
                raise EvaluationValidationError(
                    AUDIT_TRAIL_EVENT_BENCHMARK_MISMATCH_ERROR
                )

            if (
                previous_occurred_at is not None
                and event.occurred_at < previous_occurred_at
            ):
                raise EvaluationValidationError(
                    AUDIT_TRAIL_EVENT_ORDER_ERROR
                )

            previous_occurred_at = event.occurred_at