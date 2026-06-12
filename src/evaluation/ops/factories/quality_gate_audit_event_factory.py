from __future__ import annotations

from datetime import datetime

from src.evaluation.metrics.entities.experiment_result_snapshot import (
    ExperimentResultSnapshot,
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
from src.evaluation.ops.factories.audit_event_factory import (
    AuditEventFactory,
)
from src.evaluation.ops.value_objects.audit_event import (
    AuditEvent,
)
from src.evaluation.ops.value_objects.quality_gate_result import (
    QualityGateResult,
)


class QualityGateAuditEventFactory:
    """
    Factory for quality gate audit events.
    """

    @staticmethod
    def create(
        *,
        snapshot: ExperimentResultSnapshot,
        quality_gate_result: QualityGateResult,
        actor: str,
        triggered_by: AuditTrigger,
        occurred_at: datetime | None = None,
        notes: str | None = None,
    ) -> AuditEvent:
        return AuditEventFactory.create(
            event_type=AuditEventType.QUALITY_GATE_EVALUATED,
            aggregate_id=snapshot.experiment_id,
            aggregate_type=AuditAggregateType.EXPERIMENT,
            benchmark_id=snapshot.benchmark_id,
            experiment_id=snapshot.experiment_id,
            model_name=snapshot.model_name,
            actor=actor,
            action=(
                AuditAction.ALLOW
                if quality_gate_result.passed
                else AuditAction.BLOCK
            ),
            triggered_by=triggered_by,
            occurred_at=occurred_at,
            metadata={
                "gate_name": (
                    quality_gate_result.gate_name
                ),
                "passed": (
                    quality_gate_result.passed
                ),
                "severity": (
                    quality_gate_result.severity
                ),
                "message": (
                    quality_gate_result.message
                ),
            },
            notes=notes,
        )