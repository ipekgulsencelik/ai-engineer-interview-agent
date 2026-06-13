from __future__ import annotations

from datetime import datetime, timezone

from src.evaluation.ops.builders.regression_detection_result_builder import (
    RegressionDetectionResultBuilder,
)
from src.evaluation.ops.enums.audit_action import AuditAction
from src.evaluation.ops.enums.audit_event_type import AuditEventType
from src.evaluation.ops.enums.audit_trigger import AuditTrigger
from src.evaluation.ops.factories.evaluation_audit_event_factory import (
    EvaluationAuditEventFactory,
)
from src.evaluation.ops.factories.quality_gate_audit_event_factory import (
    QualityGateAuditEventFactory,
)
from src.evaluation.ops.factories.regression_audit_event_factory import (
    RegressionAuditEventFactory,
)
from src.evaluation.ops.services.evaluation_quality_gate import EvaluationQualityGate
from tests.evaluation.ops.factories import experiment_snapshot


def test_evaluation_audit_event_factory_should_create_completed_event_metadata() -> (
    None
):
    occurred_at = datetime(2026, 1, 1, tzinfo=timezone.utc)
    snapshot = experiment_snapshot(overall_score=0.86)

    event = EvaluationAuditEventFactory.create_completed(
        snapshot=snapshot,
        actor="ci",
        triggered_by=AuditTrigger.CI_PIPELINE,
        occurred_at=occurred_at,
    )

    assert event.event_type == AuditEventType.EVALUATION_COMPLETED
    assert event.action == AuditAction.EVALUATE
    assert event.occurred_at == occurred_at
    assert event.metadata["overall_score"] == 0.86


def test_quality_gate_audit_event_factory_should_block_failed_gate() -> None:
    snapshot = experiment_snapshot(overall_score=0.70)
    gate = EvaluationQualityGate().evaluate(
        gate_name="minimum_overall_score",
        snapshot=snapshot,
        minimum_required_score=0.80,
    )

    event = QualityGateAuditEventFactory.create(
        snapshot=snapshot,
        quality_gate_result=gate,
        actor="ci",
        triggered_by=AuditTrigger.USER,
    )

    assert event.event_type == AuditEventType.QUALITY_GATE_EVALUATED
    assert event.action == AuditAction.BLOCK
    assert event.metadata["passed"] is False
    assert event.metadata["message"] == "quality_gate_failed"


def test_regression_audit_event_factory_should_include_candidate_score() -> None:
    baseline = experiment_snapshot(experiment_id="baseline", overall_score=0.90)
    candidate = experiment_snapshot(experiment_id="candidate", overall_score=0.82)
    regression = RegressionDetectionResultBuilder.build(
        baseline_snapshot=baseline,
        candidate_snapshot=candidate,
        regression_threshold=0.05,
    )

    event = RegressionAuditEventFactory.create_detected(
        snapshot=candidate,
        regression_result=regression,
        actor="ci",
        triggered_by=AuditTrigger.CI_PIPELINE,
    )

    assert event.event_type == AuditEventType.REGRESSION_DETECTED
    assert event.metadata["regression_detected"] is True
    assert event.metadata["current_score"] == 0.82
