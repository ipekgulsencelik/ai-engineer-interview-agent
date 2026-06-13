from __future__ import annotations

from datetime import datetime, timezone

import pytest

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.ops.enums.audit_action import AuditAction
from src.evaluation.ops.enums.audit_aggregate_type import AuditAggregateType
from src.evaluation.ops.enums.audit_event_type import AuditEventType
from src.evaluation.ops.enums.audit_trigger import AuditTrigger
from src.evaluation.ops.validators.evaluation_audit_trail_validator import (
    EvaluationAuditTrailValidator,
)
from src.evaluation.ops.value_objects.audit_event import AuditEvent


def _event(
    *,
    event_id: str = "event-1",
    experiment_id: str = "experiment-1",
    benchmark_id: str = "benchmark-1",
    occurred_at: datetime | None = None,
) -> AuditEvent:
    return AuditEvent(
        event_id=event_id,
        event_type=AuditEventType.EVALUATION_STARTED,
        aggregate_id=experiment_id,
        aggregate_type=AuditAggregateType.EXPERIMENT,
        benchmark_id=benchmark_id,
        experiment_id=experiment_id,
        model_name="gpt-5",
        occurred_at=occurred_at or datetime(2026, 1, 1, tzinfo=timezone.utc),
        actor="ci",
        action=AuditAction.CREATE,
        triggered_by=AuditTrigger.CI_PIPELINE,
        metadata={"stage": "start"},
    )


def _valid_kwargs() -> dict[str, object]:
    return {
        "trail_id": "trail-1",
        "evaluation_run_id": "run-1",
        "experiment_id": "experiment-1",
        "benchmark_id": "benchmark-1",
        "events": (_event(),),
        "created_at": datetime(2026, 1, 1, tzinfo=timezone.utc),
    }


def test_evaluation_audit_trail_validator_should_accept_valid_payload() -> None:
    EvaluationAuditTrailValidator.validate(**_valid_kwargs())


def test_evaluation_audit_trail_validator_should_reject_non_tuple_events() -> None:
    kwargs = _valid_kwargs()
    kwargs["events"] = [_event()]

    with pytest.raises(EvaluationValidationError, match="events must be tuple"):
        EvaluationAuditTrailValidator.validate(**kwargs)


def test_evaluation_audit_trail_validator_should_reject_empty_events() -> None:
    kwargs = _valid_kwargs()
    kwargs["events"] = ()

    with pytest.raises(EvaluationValidationError, match="events cannot be empty"):
        EvaluationAuditTrailValidator.validate(**kwargs)


def test_evaluation_audit_trail_validator_should_reject_event_type_mismatch() -> None:
    kwargs = _valid_kwargs()
    kwargs["events"] = (object(),)

    with pytest.raises(EvaluationValidationError, match="events item"):
        EvaluationAuditTrailValidator.validate(**kwargs)


def test_evaluation_audit_trail_validator_should_reject_experiment_mismatch() -> None:
    kwargs = _valid_kwargs()
    kwargs["events"] = (_event(experiment_id="other-experiment"),)

    with pytest.raises(EvaluationValidationError, match="experiment_id mismatch"):
        EvaluationAuditTrailValidator.validate(**kwargs)


def test_evaluation_audit_trail_validator_should_reject_benchmark_mismatch() -> None:
    kwargs = _valid_kwargs()
    kwargs["events"] = (_event(benchmark_id="other-benchmark"),)

    with pytest.raises(EvaluationValidationError, match="benchmark_id mismatch"):
        EvaluationAuditTrailValidator.validate(**kwargs)


def test_evaluation_audit_trail_validator_should_reject_unordered_events() -> None:
    kwargs = _valid_kwargs()
    kwargs["events"] = (
        _event(
            event_id="event-2", occurred_at=datetime(2026, 1, 2, tzinfo=timezone.utc)
        ),
        _event(
            event_id="event-1", occurred_at=datetime(2026, 1, 1, tzinfo=timezone.utc)
        ),
    )

    with pytest.raises(EvaluationValidationError, match="ordered"):
        EvaluationAuditTrailValidator.validate(**kwargs)
