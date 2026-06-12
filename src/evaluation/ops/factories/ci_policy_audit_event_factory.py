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
from src.evaluation.ops.value_objects.ci_benchmark_policy_result import (
    CIBenchmarkPolicyResult,
)


class CIPolicyAuditEventFactory:
    """
    Factory for CI policy audit events.
    """

    @staticmethod
    def create(
        *,
        snapshot: ExperimentResultSnapshot,
        ci_policy_result: CIBenchmarkPolicyResult,
        actor: str,
        triggered_by: AuditTrigger,
        occurred_at: datetime | None = None,
        notes: str | None = None,
    ) -> AuditEvent:
        return AuditEventFactory.create(
            event_type=AuditEventType.CI_POLICY_EVALUATED,
            aggregate_id=snapshot.experiment_id,
            aggregate_type=AuditAggregateType.CI_POLICY,
            benchmark_id=snapshot.benchmark_id,
            experiment_id=snapshot.experiment_id,
            model_name=snapshot.model_name,
            actor=actor,
            action=(
                AuditAction.ALLOW
                if ci_policy_result.deployment_allowed
                else AuditAction.BLOCK
            ),
            triggered_by=triggered_by,
            occurred_at=occurred_at,
            metadata={
                "policy_name": (
                    ci_policy_result.policy_name
                ),
                "deployment_allowed": (
                    ci_policy_result.deployment_allowed
                ),
                "blocking_failure_count": (
                    ci_policy_result.blocking_failure_count
                ),
                "overall_score": (
                    ci_policy_result.overall_score
                ),
                "interpretation": (
                    ci_policy_result.interpretation
                ),
            },
            notes=notes,
        )