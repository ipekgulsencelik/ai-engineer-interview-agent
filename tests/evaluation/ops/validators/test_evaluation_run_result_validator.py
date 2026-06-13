from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.ops.validators.evaluation_run_result_validator import (
    EvaluationRunResultValidator,
)
from tests.evaluation.ops.factories import experiment_snapshot


def _valid_kwargs() -> dict[str, object]:
    started_at = datetime(2026, 1, 1, tzinfo=timezone.utc)
    completed_at = started_at + timedelta(seconds=5)
    return {
        "run_id": "run-1",
        "experiment_snapshot": experiment_snapshot(),
        "started_at": started_at,
        "completed_at": completed_at,
        "duration_seconds": 5.0,
        "success": True,
        "regression_result": None,
        "quality_gate_result": None,
        "ci_policy_result": None,
        "error_message": None,
        "notes": "valid run",
    }


def test_evaluation_run_result_validator_should_accept_valid_payload() -> None:
    EvaluationRunResultValidator.validate(**_valid_kwargs())


def test_evaluation_run_result_validator_should_reject_invalid_snapshot_type() -> None:
    kwargs = _valid_kwargs()
    kwargs["experiment_snapshot"] = object()

    with pytest.raises(EvaluationValidationError, match="experiment_snapshot"):
        EvaluationRunResultValidator.validate(**kwargs)


def test_evaluation_run_result_validator_should_reject_completed_before_started() -> (
    None
):
    kwargs = _valid_kwargs()
    kwargs["completed_at"] = kwargs["started_at"] - timedelta(seconds=1)  # type: ignore[operator]

    with pytest.raises(EvaluationValidationError, match="completed_at"):
        EvaluationRunResultValidator.validate(**kwargs)


def test_evaluation_run_result_validator_should_reject_duration_mismatch() -> None:
    kwargs = _valid_kwargs()
    kwargs["duration_seconds"] = 9.0

    with pytest.raises(EvaluationValidationError, match="duration_seconds mismatch"):
        EvaluationRunResultValidator.validate(**kwargs)


def test_evaluation_run_result_validator_should_require_error_for_failed_run() -> None:
    kwargs = _valid_kwargs()
    kwargs["success"] = False

    with pytest.raises(EvaluationValidationError, match="error_message"):
        EvaluationRunResultValidator.validate(**kwargs)


def test_evaluation_run_result_validator_should_accept_failed_run_with_error() -> None:
    kwargs = _valid_kwargs()
    kwargs["success"] = False
    kwargs["error_message"] = "ci_policy_failed"

    EvaluationRunResultValidator.validate(**kwargs)
