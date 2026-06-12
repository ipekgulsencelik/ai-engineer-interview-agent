from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

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
from src.evaluation.ops.types.audit_metadata import (
    AuditMetadata,
)
from src.evaluation.ops.value_objects.audit_event import (
    AuditEvent,
)


class AuditEventFactory:
    """
    Factory for creating audit events.
    """

    @staticmethod
    def create(
        *,
        event_type: AuditEventType,
        aggregate_id: str,
        aggregate_type: AuditAggregateType,
        benchmark_id: str,
        experiment_id: str,
        model_name: str,
        actor: str,
        action: AuditAction,
        triggered_by: AuditTrigger,
        metadata: AuditMetadata,
        occurred_at: datetime | None = None,
        notes: str | None = None,
    ) -> AuditEvent:
        return AuditEvent(
            event_id=str(uuid4()),
            event_type=event_type,
            aggregate_id=aggregate_id,
            aggregate_type=aggregate_type,
            benchmark_id=benchmark_id,
            experiment_id=experiment_id,
            model_name=model_name,
            occurred_at=(
                occurred_at
                or datetime.now(UTC)
            ),
            actor=actor,
            action=action,
            triggered_by=triggered_by,
            metadata=metadata,
            notes=notes,
        )