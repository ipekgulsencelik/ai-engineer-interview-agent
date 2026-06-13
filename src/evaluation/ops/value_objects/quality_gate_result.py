from __future__ import annotations

from dataclasses import dataclass

from src.evaluation.ops.validators.quality_gate_result_validator import (
    QualityGateResultValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class QualityGateResult:
    """
    Immutable quality gate result.

    Represents the result of a benchmark quality gate
    evaluation for CI/CD, regression control, and release checks.
    """

    gate_name: str

    benchmark_id: str
    benchmark_name: str
    benchmark_version: str

    experiment_id: str
    model_name: str

    metric_name: str

    actual_value: float
    expected_value: float

    passed: bool

    severity: str

    interpretation: str

    overall_score: float = 0.0
    minimum_required_score: float = 0.0

    notes: str | None = None

    def __post_init__(
        self,
    ) -> None:
        QualityGateResultValidator.validate(
            gate_name=self.gate_name,
            benchmark_id=self.benchmark_id,
            benchmark_name=self.benchmark_name,
            benchmark_version=self.benchmark_version,
            experiment_id=self.experiment_id,
            model_name=self.model_name,
            metric_name=self.metric_name,
            actual_value=self.actual_value,
            expected_value=self.expected_value,
            overall_score=self.overall_score,
            minimum_required_score=self.minimum_required_score,
            passed=self.passed,
            severity=self.severity,
            interpretation=self.interpretation,
            notes=self.notes,
        )

    @property
    def failed(
        self,
    ) -> bool:
        return not self.passed

    @property
    def value_delta(
        self,
    ) -> float:
        return self.actual_value - self.expected_value

    @property
    def absolute_value_delta(
        self,
    ) -> float:
        return abs(
            self.value_delta,
        )

    @property
    def score_margin(
        self,
    ) -> float:
        return self.overall_score - self.minimum_required_score

    @property
    def meets_score_requirement(
        self,
    ) -> bool:
        return self.overall_score >= self.minimum_required_score
