from __future__ import annotations

from datetime import datetime

from src.evaluation.metrics.entities.experiment_result_snapshot import (
    ExperimentResultSnapshot,
)
from src.evaluation.ops.builders.evaluation_audit_trail_builder import (
    EvaluationAuditTrailBuilder,
)
from src.evaluation.ops.entities.evaluation_audit_trail import EvaluationAuditTrail
from src.evaluation.ops.value_objects.audit_event import AuditEvent


class EvaluationAuditService:
    """
    Evaluation audit orchestration service.
    """

    def __init__(
        self,
        *,
        trail_builder: EvaluationAuditTrailBuilder | None = None,
    ) -> None:
        self._trail_builder = trail_builder or EvaluationAuditTrailBuilder()

    def create_audit_trail(
        self,
        *,
        evaluation_run_id: str,
        snapshot: ExperimentResultSnapshot,
        events: tuple[AuditEvent, ...],
        created_at: datetime | None = None,
    ) -> EvaluationAuditTrail:
        return self._trail_builder.build(
            evaluation_run_id=evaluation_run_id,
            snapshot=snapshot,
            events=events,
            created_at=created_at,
        )
