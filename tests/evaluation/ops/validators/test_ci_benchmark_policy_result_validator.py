from __future__ import annotations

import pytest

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.ops.validators.ci_benchmark_policy_result_validator import (
    CIBenchmarkPolicyResultValidator,
)
from src.evaluation.ops.value_objects.quality_gate_result import QualityGateResult


def _gate(*, passed: bool = True, severity: str = "info") -> QualityGateResult:
    return QualityGateResult(
        gate_name="minimum_overall_score",
        benchmark_id="benchmark-1",
        benchmark_name="AI Engineer Benchmark",
        benchmark_version="1.0.0",
        experiment_id="experiment-1",
        model_name="gpt-5",
        metric_name="overall_score",
        actual_value=0.91 if passed else 0.70,
        expected_value=0.80,
        overall_score=0.91 if passed else 0.70,
        minimum_required_score=0.80,
        passed=passed,
        severity=severity,
        interpretation="quality_gate_passed" if passed else "quality_gate_failed",
    )


def _valid_kwargs() -> dict[str, object]:
    return {
        "policy_name": "release_policy",
        "benchmark_id": "benchmark-1",
        "benchmark_name": "AI Engineer Benchmark",
        "benchmark_version": "1.0.0",
        "benchmark_score": 0.91,
        "minimum_required_score": 0.80,
        "experiment_id": "experiment-1",
        "overall_score": 0.91,
        "gate_results": (_gate(),),
        "blocking_failure_count": 0,
        "deployment_allowed": True,
        "interpretation": "ci_policy_passed",
        "notes": "valid result",
    }


def test_ci_benchmark_policy_result_validator_should_accept_valid_payload() -> None:
    CIBenchmarkPolicyResultValidator.validate(**_valid_kwargs())


def test_ci_benchmark_policy_result_validator_should_reject_non_tuple_gate_results() -> (
    None
):
    kwargs = _valid_kwargs()
    kwargs["gate_results"] = [_gate()]

    with pytest.raises(EvaluationValidationError, match="gate_results must be tuple"):
        CIBenchmarkPolicyResultValidator.validate(**kwargs)


def test_ci_benchmark_policy_result_validator_should_reject_invalid_gate_item() -> None:
    kwargs = _valid_kwargs()
    kwargs["gate_results"] = (object(),)

    with pytest.raises(EvaluationValidationError, match=r"gate_results\[0\]"):
        CIBenchmarkPolicyResultValidator.validate(**kwargs)


def test_ci_benchmark_policy_result_validator_should_reject_failure_count_mismatch() -> (
    None
):
    kwargs = _valid_kwargs()
    kwargs["gate_results"] = (_gate(passed=False, severity="critical"),)
    kwargs["benchmark_score"] = 0.70
    kwargs["overall_score"] = 0.70
    kwargs["deployment_allowed"] = False
    kwargs["blocking_failure_count"] = 0

    with pytest.raises(EvaluationValidationError, match="blocking_failure_count"):
        CIBenchmarkPolicyResultValidator.validate(**kwargs)


def test_ci_benchmark_policy_result_validator_should_reject_deployment_mismatch() -> (
    None
):
    kwargs = _valid_kwargs()
    kwargs["deployment_allowed"] = False

    with pytest.raises(EvaluationValidationError, match="deployment_allowed"):
        CIBenchmarkPolicyResultValidator.validate(**kwargs)
