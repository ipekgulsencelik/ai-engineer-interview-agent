from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from src.evaluation.metrics.entities.experiment_result_snapshot import (
    ExperimentResultSnapshot,
)
from src.evaluation.ops.validators.evaluation_run_result_validator import (
    EvaluationRunResultValidator,
)
from src.evaluation.ops.value_objects.ci_benchmark_policy_result import (
    CIBenchmarkPolicyResult,
)
from src.evaluation.ops.value_objects.quality_gate_result import QualityGateResult
from src.evaluation.ops.value_objects.regression_detection_result import (
    RegressionDetectionResult,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class EvaluationRunResult:
    """
    Immutable evaluation run result.
    """

    run_id: str
    experiment_snapshot: ExperimentResultSnapshot
    started_at: datetime
    completed_at: datetime
    duration_seconds: float
    success: bool
    regression_result: RegressionDetectionResult | None = None
    quality_gate_result: QualityGateResult | None = None
    ci_policy_result: CIBenchmarkPolicyResult | None = None
    error_message: str | None = None
    notes: str | None = None

    def __post_init__(self) -> None:
        EvaluationRunResultValidator.validate(
            run_id=self.run_id,
            experiment_snapshot=self.experiment_snapshot,
            started_at=self.started_at,
            completed_at=self.completed_at,
            duration_seconds=self.duration_seconds,
            success=self.success,
            regression_result=self.regression_result,
            quality_gate_result=self.quality_gate_result,
            ci_policy_result=self.ci_policy_result,
            error_message=self.error_message,
            notes=self.notes,
        )

    @property
    def experiment_id(self) -> str:
        return self.experiment_snapshot.experiment_id

    @property
    def benchmark_id(self) -> str:
        return self.experiment_snapshot.benchmark_id

    @property
    def benchmark_name(self) -> str:
        return self.experiment_snapshot.benchmark_name

    @property
    def benchmark_version(self) -> str:
        return self.experiment_snapshot.benchmark_version

    @property
    def model_name(self) -> str:
        return self.experiment_snapshot.model_name

    @property
    def overall_score(self) -> float:
        return self.experiment_snapshot.overall_score

    @property
    def ci_passed(self) -> bool | None:
        if self.ci_policy_result is None:
            return None
        return self.ci_policy_result.deployment_allowed

    @property
    def has_ci_policy(self) -> bool:
        return self.ci_policy_result is not None

    @property
    def deployment_allowed(self) -> bool | None:
        if self.ci_policy_result is None:
            return None
        return self.ci_policy_result.deployment_allowed

    @property
    def has_blocking_failures(self) -> bool | None:
        if self.ci_policy_result is None:
            return None
        return self.ci_policy_result.has_blocking_failures

    @property
    def blocking_failure_count(self) -> int | None:
        if self.ci_policy_result is None:
            return None
        return self.ci_policy_result.blocking_failure_count

    @property
    def ci_interpretation(self) -> str | None:
        if self.ci_policy_result is None:
            return None
        return self.ci_policy_result.interpretation
