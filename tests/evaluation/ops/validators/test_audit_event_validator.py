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
from src.evaluation.ops.validators.audit_event_validator import AuditEventValidator


def _valid_kwargs() -> dict[str, object]:
    return {
        "event_id": "event-1",
        "event_type": AuditEventType.EVALUATION_STARTED,
        "aggregate_id": "experiment-1",
        "aggregate_type": AuditAggregateType.EXPERIMENT,
        "benchmark_id": "benchmark-1",
        "experiment_id": "experiment-1",
        "model_name": "gpt-5",
        "occurred_at": datetime(2026, 1, 1, tzinfo=timezone.utc),
        "actor": "ci",
        "action": AuditAction.CREATE,
        "triggered_by": AuditTrigger.CI_PIPELINE,
        "metadata": {
            "stage": "start",
            "attempt": 1,
            "score": 0.91,
            "passed": True,
        },
        "notes": "valid audit event",
    }


def test_audit_event_validator_should_accept_valid_payload() -> None:
    AuditEventValidator.validate(**_valid_kwargs())


@pytest.mark.parametrize(
    "field_name",
    [
        "event_id",
        "aggregate_id",
        "benchmark_id",
        "experiment_id",
        "model_name",
        "actor",
    ],
)
def test_audit_event_validator_should_reject_empty_string_fields(
    field_name: str,
) -> None:
    kwargs = _valid_kwargs()
    kwargs[field_name] = ""

    with pytest.raises(EvaluationValidationError):
        AuditEventValidator.validate(**kwargs)


@pytest.mark.parametrize(
    ("field_name", "invalid_value"),
    [
        ("event_type", "evaluation_started"),
        ("aggregate_type", "experiment"),
        ("action", "create"),
        ("triggered_by", "ci_pipeline"),
    ],
)
def test_audit_event_validator_should_reject_non_enum_values(
    field_name: str,
    invalid_value: object,
) -> None:
    kwargs = _valid_kwargs()
    kwargs[field_name] = invalid_value

    with pytest.raises(EvaluationValidationError):
        AuditEventValidator.validate(**kwargs)


def test_audit_event_validator_should_reject_non_mapping_metadata() -> None:
    kwargs = _valid_kwargs()
    kwargs["metadata"] = [("stage", "start")]

    with pytest.raises(EvaluationValidationError, match="metadata must be a mapping"):
        AuditEventValidator.validate(**kwargs)


def test_audit_event_validator_should_reject_non_string_metadata_keys() -> None:
    kwargs = _valid_kwargs()
    kwargs["metadata"] = {1: "start"}

    with pytest.raises(EvaluationValidationError, match="metadata keys"):
        AuditEventValidator.validate(**kwargs)


def test_audit_event_validator_should_reject_invalid_metadata_values() -> None:
    kwargs = _valid_kwargs()
    kwargs["metadata"] = {"payload": {"nested": "value"}}

    with pytest.raises(EvaluationValidationError, match="metadata values"):
        AuditEventValidator.validate(**kwargs)
