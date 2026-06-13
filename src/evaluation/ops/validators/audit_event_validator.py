from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime

from src.domain.validators.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.ops.constants.audit_event import (
    AUDIT_ACTION_TYPE_ERROR,
    AUDIT_AGGREGATE_TYPE_ERROR,
    AUDIT_EVENT_TYPE_ERROR,
    AUDIT_METADATA_KEY_TYPE_ERROR,
    AUDIT_METADATA_TYPE_ERROR,
    AUDIT_METADATA_VALUE_TYPE_ERROR,
    AUDIT_TRIGGER_TYPE_ERROR,
)
from src.evaluation.ops.enums.audit_action import (
    AuditAction,
)
from src.evaluation.ops.enums.audit_aggregate_type import (
    AuditAggregateType,
)
from src.evaluation.ops.enums.audit_event_type import (
    AuditEventType,
)
from src.evaluation.ops.enums.audit_trigger import (
    AuditTrigger,
)
from src.evaluation.ops.schemas.audit_event_schema import (
    AUDIT_EVENT_SCHEMA,
)


class AuditEventValidator:
    """
    AuditEvent validation service.
    """

    @staticmethod
    def validate(
        *,
        event_id: str,
        event_type: AuditEventType,
        aggregate_id: str,
        aggregate_type: AuditAggregateType,
        benchmark_id: str,
        experiment_id: str,
        model_name: str,
        occurred_at: datetime,
        actor: str,
        action: AuditAction,
        triggered_by: AuditTrigger,
        metadata: Mapping[str, object],
        notes: str | None = None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "event_id": event_id,
                "aggregate_id": aggregate_id,
                "benchmark_id": benchmark_id,
                "experiment_id": experiment_id,
                "model_name": model_name,
                "occurred_at": occurred_at,
                "actor": actor,
                "notes": notes,
            },
            schema=AUDIT_EVENT_SCHEMA,
            error_factory=EvaluationValidationError,
        )

        if not isinstance(
            event_type,
            AuditEventType,
        ):
            raise EvaluationValidationError(
                AUDIT_EVENT_TYPE_ERROR
            )

        if not isinstance(
            aggregate_type,
            AuditAggregateType,
        ):
            raise EvaluationValidationError(
                AUDIT_AGGREGATE_TYPE_ERROR
            )

        if not isinstance(
            action,
            AuditAction,
        ):
            raise EvaluationValidationError(
                AUDIT_ACTION_TYPE_ERROR
            )

        if not isinstance(
            triggered_by,
            AuditTrigger,
        ):
            raise EvaluationValidationError(
                AUDIT_TRIGGER_TYPE_ERROR
            )

        if not isinstance(
            metadata,
            Mapping,
        ):
            raise EvaluationValidationError(
                AUDIT_METADATA_TYPE_ERROR
            )

        for key, value in metadata.items():
            if not isinstance(
                key,
                str,
            ):
                raise EvaluationValidationError(
                    AUDIT_METADATA_KEY_TYPE_ERROR
                )

            if not isinstance(
                value,
                str | int | float | bool,
            ):
                raise EvaluationValidationError(
                    AUDIT_METADATA_VALUE_TYPE_ERROR
                )