from __future__ import annotations

from src.evaluation.ops.evaluators.ci_policy_evaluator import CIPolicyEvaluator
from src.evaluation.ops.evaluators.quality_gate_evaluator import QualityGateEvaluator
from src.evaluation.ops.evaluators.run_success_evaluator import RunSuccessEvaluator
from src.evaluation.ops.services.ci_benchmark_policy import CIBenchmarkPolicy
from tests.evaluation.ops.factories import experiment_snapshot


def test_quality_gate_evaluator_should_pass_at_threshold() -> None:
    assert QualityGateEvaluator.evaluate(score=0.80, minimum_required_score=0.80)


def test_ci_policy_evaluator_should_block_when_failures_exist() -> None:
    assert CIPolicyEvaluator.evaluate(blocking_failure_count=0) is True
    assert CIPolicyEvaluator.evaluate(blocking_failure_count=1) is False


def test_run_success_evaluator_should_follow_ci_deployment_decision() -> None:
    passing_result = CIBenchmarkPolicy().evaluate(
        policy_name="policy",
        snapshot=experiment_snapshot(overall_score=0.90),
        minimum_required_score=0.80,
    )
    failing_result = CIBenchmarkPolicy().evaluate(
        policy_name="policy",
        snapshot=experiment_snapshot(overall_score=0.70),
        minimum_required_score=0.80,
    )

    assert RunSuccessEvaluator.evaluate(ci_policy_result=None) is True
    assert RunSuccessEvaluator.evaluate(ci_policy_result=passing_result) is True
    assert RunSuccessEvaluator.evaluate(ci_policy_result=failing_result) is False
