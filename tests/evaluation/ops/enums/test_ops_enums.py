from __future__ import annotations

from src.evaluation.ops.enums.audit_action import AuditAction
from src.evaluation.ops.enums.audit_aggregate_type import AuditAggregateType
from src.evaluation.ops.enums.audit_event_type import AuditEventType
from src.evaluation.ops.enums.audit_trigger import AuditTrigger
from src.evaluation.ops.enums.dashboard_severity import DashboardSeverity


def test_ops_enums_should_expose_stable_string_values() -> None:
    assert AuditAction.BLOCK == "block"
    assert AuditAggregateType.CI_POLICY == "ci_policy"
    assert AuditEventType.CI_POLICY_EVALUATED == "ci_policy_evaluated"
    assert AuditTrigger.SCHEDULED_JOB == "scheduled_job"
    assert DashboardSeverity.CRITICAL == "critical"
