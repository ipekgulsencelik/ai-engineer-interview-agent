from __future__ import annotations

import pytest

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.ops.value_objects.quality_gate_result import QualityGateResult


def test_quality_gate_result_should_expose_failure_and_delta_helpers() -> None:
    result = QualityGateResult(
        gate_name="minimum-overall-score",
        benchmark_id="benchmark-1",
        benchmark_name="AI Engineer Benchmark",
        benchmark_version="1.0.0",
        experiment_id="experiment-1",
        model_name="gpt-5",
        metric_name="overall_score",
        actual_value=0.78,
        expected_value=0.80,
        passed=False,
        severity="critical",
        interpretation="below_threshold",
    )

    assert result.failed is True
    assert result.value_delta == pytest.approx(-0.02)
    assert result.absolute_value_delta == pytest.approx(0.02)


def test_quality_gate_result_should_raise_for_empty_gate_name() -> None:
    with pytest.raises(EvaluationValidationError):
        QualityGateResult(
            gate_name="",
            benchmark_id="benchmark-1",
            benchmark_name="AI Engineer Benchmark",
            benchmark_version="1.0.0",
            experiment_id="experiment-1",
            model_name="gpt-5",
            metric_name="overall_score",
            actual_value=0.78,
            expected_value=0.80,
            passed=False,
            severity="critical",
            interpretation="below_threshold",
        )
