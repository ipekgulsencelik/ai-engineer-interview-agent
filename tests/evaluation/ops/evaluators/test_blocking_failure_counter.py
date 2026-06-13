from __future__ import annotations

from src.evaluation.ops.evaluators.blocking_failure_counter import (
    BlockingFailureCounter,
)
from src.evaluation.ops.value_objects.quality_gate_result import QualityGateResult


def _gate(*, passed: bool, severity: str) -> QualityGateResult:
    return QualityGateResult(
        gate_name="minimum_overall_score",
        benchmark_id="benchmark-1",
        benchmark_name="AI Engineer Benchmark",
        benchmark_version="1.0.0",
        experiment_id="experiment-1",
        model_name="gpt-5",
        metric_name="overall_score",
        actual_value=0.90 if passed else 0.70,
        expected_value=0.80,
        overall_score=0.90 if passed else 0.70,
        minimum_required_score=0.80,
        passed=passed,
        severity=severity,
        interpretation="quality_gate_passed" if passed else "quality_gate_failed",
    )


def test_blocking_failure_counter_should_count_only_failed_critical_gates() -> None:
    assert (
        BlockingFailureCounter.count(
            gate_results=(
                _gate(passed=False, severity="critical"),
                _gate(passed=False, severity="warning"),
                _gate(passed=True, severity="critical"),
            ),
        )
        == 1
    )
