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
from src.evaluation.ops.value_objects.regression_detection_result import (
    RegressionDetectionResult,
)


class RegressionAuditEventFactory:
    """
    Factory for regression audit events.
    """

    @staticmethod
    def create_detected(
        *,
        snapshot: ExperimentResultSnapshot,
        regression_result: RegressionDetectionResult,
        actor: str,
        triggered_by: AuditTrigger,
        occurred_at: datetime | None = None,
        notes: str | None = None,
    ) -> AuditEvent:
        return AuditEventFactory.create(
            event_type=AuditEventType.REGRESSION_DETECTED,
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
                "regression_detected": (
                    regression_result.regression_detected
                ),
                "baseline_score": (
                    regression_result.baseline_score
                ),
                "current_score": (
                    regression_result.current_score
                ),
                "score_delta": (
                    regression_result.score_delta
                ),
            },
            notes=notes,
        )