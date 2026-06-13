from __future__ import annotations

from datetime import datetime, timezone

from src.evaluation.ops.enums.audit_action import AuditAction
from src.evaluation.ops.enums.audit_aggregate_type import AuditAggregateType
from src.evaluation.ops.enums.audit_event_type import AuditEventType
from src.evaluation.ops.enums.audit_trigger import AuditTrigger
from src.evaluation.ops.factories.audit_event_factory import AuditEventFactory
from src.evaluation.ops.factories.ci_policy_audit_event_factory import (
    CIPolicyAuditEventFactory,
)
from src.evaluation.ops.services.ci_benchmark_policy import CIBenchmarkPolicy
from tests.evaluation.ops.factories import experiment_snapshot


def test_audit_event_factory_should_create_event_with_supplied_timestamp() -> None:
    occurred_at = datetime(2026, 1, 1, tzinfo=timezone.utc)

    event = AuditEventFactory.create(
        event_type=AuditEventType.EVALUATION_STARTED,
        aggregate_id="experiment-1",
        aggregate_type=AuditAggregateType.EXPERIMENT,
        benchmark_id="benchmark-1",
        experiment_id="experiment-1",
        model_name="gpt-5",
        actor="ci",
        action=AuditAction.CREATE,
        triggered_by=AuditTrigger.CI_PIPELINE,
        metadata={"stage": "start"},
        occurred_at=occurred_at,
        notes="created",
    )

    assert event.event_id
    assert event.occurred_at == occurred_at
    assert event.metadata["stage"] == "start"
    assert event.notes == "created"


def test_ci_policy_audit_event_factory_should_allow_successful_policy() -> None:
    snapshot = experiment_snapshot(overall_score=0.91)
    ci_policy_result = CIBenchmarkPolicy().evaluate(
        policy_name="release_policy",
        snapshot=snapshot,
        minimum_required_score=0.80,
    )

    event = CIPolicyAuditEventFactory.create(
        snapshot=snapshot,
        ci_policy_result=ci_policy_result,
        actor="ci",
        triggered_by=AuditTrigger.CI_PIPELINE,
    )

    assert event.event_type == AuditEventType.CI_POLICY_EVALUATED
    assert event.aggregate_type == AuditAggregateType.CI_POLICY
    assert event.action == AuditAction.ALLOW
    assert event.metadata["policy_name"] == "release_policy"
    assert event.metadata["deployment_allowed"] is True
    assert event.metadata["blocking_failure_count"] == 0
