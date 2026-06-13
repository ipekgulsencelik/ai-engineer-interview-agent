from __future__ import annotations

from src.evaluation.ops.value_objects.ci_benchmark_policy_result import (
    CIBenchmarkPolicyResult,
)


class RunSuccessEvaluator:
    """
    Evaluation run success evaluator.
    """

    @staticmethod
    def evaluate(
        *,
        ci_policy_result: (CIBenchmarkPolicyResult | None),
    ) -> bool:
        if ci_policy_result is None:
            return True

        return ci_policy_result.deployment_allowed
