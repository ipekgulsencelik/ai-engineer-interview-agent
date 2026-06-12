from __future__ import annotations

from dataclasses import dataclass

from src.evaluation.ops.validators.ci_benchmark_policy_result_validator import (
    CIBenchmarkPolicyResultValidator,
)
from src.evaluation.ops.value_objects.quality_gate_result import (
    QualityGateResult,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class CIBenchmarkPolicyResult:
    """
    Immutable CI benchmark policy result.

    Represents the final benchmark policy evaluation
    executed inside CI/CD pipelines.
    """

    policy_name: str

    benchmark_id: str
    benchmark_name: str
    benchmark_version: str

    benchmark_score: float
    minimum_required_score: float

    experiment_id: str

    overall_score: float

    gate_results: tuple[
        QualityGateResult,
        ...,
    ]

    blocking_failure_count: int

    deployment_allowed: bool

    interpretation: str

    notes: str | None = None

    def __post_init__(
        self,
    ) -> None:
        CIBenchmarkPolicyResultValidator.validate(
            policy_name=self.policy_name,
            benchmark_id=self.benchmark_id,
            benchmark_name=self.benchmark_name,
            benchmark_version=self.benchmark_version,
            benchmark_score=self.benchmark_score,
            minimum_required_score=(
                self.minimum_required_score
            ),
            experiment_id=self.experiment_id,
            overall_score=self.overall_score,
            gate_results=self.gate_results,
            blocking_failure_count=(
                self.blocking_failure_count
            ),
            deployment_allowed=(
                self.deployment_allowed
            ),
            interpretation=self.interpretation,
            notes=self.notes,
        )

    @property
    def total_gate_count(
        self,
    ) -> int:
        return len(
            self.gate_results,
        )

    @property
    def passed_gate_count(
        self,
    ) -> int:
        return sum(
            gate.passed
            for gate in self.gate_results
        )

    @property
    def failed_gate_count(
        self,
    ) -> int:
        return sum(
            not gate.passed
            for gate in self.gate_results
        )

    @property
    def pass_rate(
        self,
    ) -> float:
        if not self.gate_results:
            return 0.0

        return (
            self.passed_gate_count
            / self.total_gate_count
        )

    @property
    def has_blocking_failures(
        self,
    ) -> bool:
        return (
            self.blocking_failure_count > 0
        )