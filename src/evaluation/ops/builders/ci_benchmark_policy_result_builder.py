from __future__ import annotations

from src.evaluation.metrics.entities.experiment_result_snapshot import (
    ExperimentResultSnapshot,
)
from src.evaluation.ops.value_objects.ci_benchmark_policy_result import (
    CIBenchmarkPolicyResult,
)
from src.evaluation.ops.value_objects.quality_gate_result import (
    QualityGateResult,
)


class CIBenchmarkPolicyResultBuilder:
    """
    Builds CI benchmark policy results.
    """

    @staticmethod
    def build(
        *,
        policy_name: str,
        snapshot: ExperimentResultSnapshot,
        minimum_required_score: float,
        gate_results: tuple[
            QualityGateResult,
            ...,
        ],
        blocking_failure_count: int,
        deployment_allowed: bool,
        notes: str | None = None,
    ) -> CIBenchmarkPolicyResult:
        return CIBenchmarkPolicyResult(
            policy_name=policy_name,
            benchmark_id=snapshot.benchmark_id,
            benchmark_name=snapshot.benchmark_name,
            benchmark_version=snapshot.benchmark_version,
            benchmark_score=snapshot.overall_score,
            minimum_required_score=(
                minimum_required_score
            ),
            experiment_id=snapshot.experiment_id,
            overall_score=snapshot.overall_score,
            gate_results=gate_results,
            blocking_failure_count=(
                blocking_failure_count
            ),
            deployment_allowed=(
                deployment_allowed
            ),
            interpretation=(
                "ci_policy_passed"
                if deployment_allowed
                else "ci_policy_failed"
            ),
            notes=notes,
        )