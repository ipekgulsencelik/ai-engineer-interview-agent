from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from src.evaluation.metrics.entities.experiment_result_snapshot import (
    ExperimentResultSnapshot,
)
from src.evaluation.ops.entities.evaluation_audit_trail import (
    EvaluationAuditTrail,
)
from src.evaluation.ops.value_objects.audit_event import (
    AuditEvent,
)


class EvaluationAuditTrailBuilder:
    """
    Builds evaluation audit trails.
    """

    @staticmethod
    def build(
        *,
        evaluation_run_id: str,
        snapshot: ExperimentResultSnapshot,
        events: tuple[
            AuditEvent,
            ...,
        ],
        created_at: datetime | None = None,
    ) -> EvaluationAuditTrail:
        return EvaluationAuditTrail(
            trail_id=str(uuid4()),
            evaluation_run_id=evaluation_run_id,
            experiment_id=snapshot.experiment_id,
            benchmark_id=snapshot.benchmark_id,
            events=events,
            created_at=(
                created_at
                or datetime.now(UTC)
            ),
        )