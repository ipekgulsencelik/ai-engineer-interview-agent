from __future__ import annotations

import pytest

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.ops.validators.ci_benchmark_policy_input_validator import (
    CIBenchmarkPolicyInputValidator,
)
from src.evaluation.ops.value_objects.quality_gate_result import QualityGateResult
from tests.evaluation.ops.factories import experiment_snapshot


def _gate() -> QualityGateResult:
    return QualityGateResult(
        gate_name="custom_gate",
        benchmark_id="benchmark-1",
        benchmark_name="AI Engineer Benchmark",
        benchmark_version="1.0.0",
        experiment_id="experiment-1",
        model_name="gpt-5",
        metric_name="overall_score",
        actual_value=0.91,
        expected_value=0.80,
        overall_score=0.91,
        minimum_required_score=0.80,
        passed=True,
        severity="info",
        interpretation="quality_gate_passed",
    )


def test_ci_benchmark_policy_input_validator_should_accept_valid_input() -> None:
    CIBenchmarkPolicyInputValidator.validate(
        snapshot=experiment_snapshot(),
        additional_gate_results=(_gate(),),
    )


def test_ci_benchmark_policy_input_validator_should_reject_invalid_snapshot() -> None:
    with pytest.raises(EvaluationValidationError, match="snapshot"):
        CIBenchmarkPolicyInputValidator.validate(
            snapshot=object(),  # type: ignore[arg-type]
            additional_gate_results=(),
        )


def test_ci_benchmark_policy_input_validator_should_reject_invalid_gate_items() -> None:
    with pytest.raises(
        EvaluationValidationError, match=r"additional_gate_results\[0\]"
    ):
        CIBenchmarkPolicyInputValidator.validate(
            snapshot=experiment_snapshot(),
            additional_gate_results=(object(),),  # type: ignore[arg-type]
        )
