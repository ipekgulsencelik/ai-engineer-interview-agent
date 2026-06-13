from __future__ import annotations

import pytest

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.ops.validators.quality_gate_result_validator import (
    QualityGateResultValidator,
)


def _valid_kwargs() -> dict[str, object]:
    return {
        "gate_name": "minimum-overall-score",
        "benchmark_id": "benchmark-1",
        "benchmark_name": "AI Engineer Benchmark",
        "benchmark_version": "1.0.0",
        "experiment_id": "experiment-1",
        "model_name": "gpt-5",
        "metric_name": "overall_score",
        "actual_value": 0.80,
        "expected_value": 0.75,
        "overall_score": 0.80,
        "minimum_required_score": 0.75,
        "passed": True,
        "severity": "critical",
        "interpretation": "above_threshold",
        "notes": "Valid quality gate.",
    }


def test_quality_gate_result_validator_should_accept_valid_payload() -> None:
    QualityGateResultValidator.validate(**_valid_kwargs())


@pytest.mark.parametrize(
    "field_name",
    [
        "gate_name",
        "benchmark_id",
        "benchmark_name",
        "benchmark_version",
        "experiment_id",
        "model_name",
        "metric_name",
        "severity",
        "interpretation",
    ],
)
def test_quality_gate_result_validator_should_reject_empty_strings(
    field_name: str,
) -> None:
    kwargs = _valid_kwargs()
    kwargs[field_name] = ""

    with pytest.raises(EvaluationValidationError):
        QualityGateResultValidator.validate(**kwargs)


def test_quality_gate_result_validator_should_reject_boolean_numeric_values() -> None:
    kwargs = _valid_kwargs()
    kwargs["actual_value"] = True

    with pytest.raises(EvaluationValidationError):
        QualityGateResultValidator.validate(**kwargs)


def test_quality_gate_result_validator_should_reject_non_boolean_passed() -> None:
    kwargs = _valid_kwargs()
    kwargs["passed"] = "yes"

    with pytest.raises(EvaluationValidationError):
        QualityGateResultValidator.validate(**kwargs)
