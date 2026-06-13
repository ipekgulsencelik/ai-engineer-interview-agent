from __future__ import annotations

from src.api.schemas.evaluation.ci_policy_summary_response import (
    CIPolicySummaryResponse,
)
from src.evaluation.ops.value_objects.ci_benchmark_policy_result import (
    CIBenchmarkPolicyResult,
)


class CIPolicySummaryResponseMapper:
    """
    Maps CI benchmark policy results.
    """

    @staticmethod
    def map(
        *,
        ci_policy_result: (
            CIBenchmarkPolicyResult
        ),
    ) -> CIPolicySummaryResponse:
        return CIPolicySummaryResponse(
            passed=ci_policy_result.passed,
            blocking_failure_count=(
                ci_policy_result.blocking_failure_count
            ),
            interpretation=(
                ci_policy_result.interpretation
            ),
        )