from __future__ import annotations

from datetime import datetime, timezone

from src.evaluation.ops.enums.audit_action import AuditAction
from src.evaluation.ops.enums.audit_aggregate_type import AuditAggregateType
from src.evaluation.ops.enums.audit_event_type import AuditEventType
from src.evaluation.ops.enums.audit_trigger import AuditTrigger
from src.evaluation.ops.services.evaluation_audit_service import EvaluationAuditService
from src.evaluation.ops.services.evaluation_quality_gate import EvaluationQualityGate
from src.evaluation.ops.value_objects.audit_event import AuditEvent
from tests.evaluation.ops.factories import experiment_snapshot


def test_evaluation_quality_gate_should_use_expected_value_override() -> None:
    snapshot = experiment_snapshot(overall_score=0.82)

    result = EvaluationQualityGate().evaluate(
        gate_name="minimum_overall_score",
        snapshot=snapshot,
        minimum_required_score=0.80,
        expected_value=0.85,
        notes="custom expectation",
    )

    assert result.actual_value == 0.82
    assert result.expected_value == 0.85
    assert result.minimum_required_score == 0.80
    assert result.passed is True
    assert result.notes == "custom expectation"


def test_evaluation_audit_service_should_create_trail_with_default_builder() -> None:
    occurred_at = datetime(2026, 1, 1, tzinfo=timezone.utc)
    snapshot = experiment_snapshot()
    event = AuditEvent(
        event_id="event-1",
        event_type=AuditEventType.EVALUATION_STARTED,
        aggregate_id=snapshot.experiment_id,
        aggregate_type=AuditAggregateType.EXPERIMENT,
        benchmark_id=snapshot.benchmark_id,
        experiment_id=snapshot.experiment_id,
        model_name=snapshot.model_name,
        occurred_at=occurred_at,
        actor="ci",
        action=AuditAction.CREATE,
        triggered_by=AuditTrigger.CI_PIPELINE,
        metadata={"stage": "start"},
    )

    trail = EvaluationAuditService().create_audit_trail(
        evaluation_run_id="run-1",
        snapshot=snapshot,
        events=(event,),
        created_at=occurred_at,
    )

    assert trail.evaluation_run_id == "run-1"
    assert trail.events == (event,)
    assert trail.created_at == occurred_at
