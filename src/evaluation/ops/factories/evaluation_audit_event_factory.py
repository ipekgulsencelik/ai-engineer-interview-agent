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


class EvaluationAuditEventFactory:
    """
    Factory for evaluation lifecycle audit events.
    """

    @staticmethod
    def create_started(
        *,
        snapshot: ExperimentResultSnapshot,
        actor: str,
        triggered_by: AuditTrigger,
        occurred_at: datetime | None = None,
        notes: str | None = None,
    ) -> AuditEvent:
        return AuditEventFactory.create(
            event_type=AuditEventType.EVALUATION_STARTED,
            aggregate_id=snapshot.experiment_id,
            aggregate_type=AuditAggregateType.EXPERIMENT,
            benchmark_id=snapshot.benchmark_id,
            experiment_id=snapshot.experiment_id,
            model_name=snapshot.model_name,
            actor=actor,
            action=AuditAction.CREATE,
            triggered_by=triggered_by,
            occurred_at=occurred_at,
            metadata={
                "benchmark_name": snapshot.benchmark_name,
                "benchmark_version": snapshot.benchmark_version,
            },
            notes=notes,
        )

    @staticmethod
    def create_completed(
        *,
        snapshot: ExperimentResultSnapshot,
        actor: str,
        triggered_by: AuditTrigger,
        occurred_at: datetime | None = None,
        notes: str | None = None,
    ) -> AuditEvent:
        return AuditEventFactory.create(
            event_type=AuditEventType.EVALUATION_COMPLETED,
            aggregate_id=snapshot.experiment_id,
            aggregate_type=AuditAggregateType.EXPERIMENT,
            benchmark_id=snapshot.benchmark_id,
            experiment_id=snapshot.experiment_id,
            model_name=snapshot.model_name,
            actor=actor,
            action=AuditAction.EVALUATE,
            triggered_by=triggered_by,
            occurred_at=occurred_at,
            metadata={
                "benchmark_name": snapshot.benchmark_name,
                "benchmark_version": snapshot.benchmark_version,
                "overall_score": snapshot.overall_score,
            },
            notes=notes,
        )

    @staticmethod
    def create_failed(
        *,
        snapshot: ExperimentResultSnapshot,
        actor: str,
        triggered_by: AuditTrigger,
        error_message: str,
        occurred_at: datetime | None = None,
        notes: str | None = None,
    ) -> AuditEvent:
        return AuditEventFactory.create(
            event_type=AuditEventType.EVALUATION_FAILED,
            aggregate_id=snapshot.experiment_id,
            aggregate_type=AuditAggregateType.EXPERIMENT,
            benchmark_id=snapshot.benchmark_id,
            experiment_id=snapshot.experiment_id,
            model_name=snapshot.model_name,
            actor=actor,
            action=AuditAction.EVALUATE,
            triggered_by=triggered_by,
            occurred_at=occurred_at,
            metadata={
                "benchmark_name": snapshot.benchmark_name,
                "benchmark_version": snapshot.benchmark_version,
                "error_message": error_message,
            },
            notes=notes,
        )