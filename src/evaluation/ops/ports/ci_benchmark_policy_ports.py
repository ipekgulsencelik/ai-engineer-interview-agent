from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol

from src.evaluation.metrics.entities.experiment_result_snapshot import (
    ExperimentResultSnapshot,
)
from src.evaluation.ops.value_objects.ci_benchmark_policy_result import (
    CIBenchmarkPolicyResult,
)
from src.evaluation.ops.value_objects.quality_gate_result import QualityGateResult


class CIBenchmarkPolicyInputValidation(Protocol):
    def validate(
        self,
        *,
        snapshot: ExperimentResultSnapshot,
        additional_gate_results: Sequence[QualityGateResult],
    ) -> None: ...


class QualityGateEvaluation(Protocol):
    def evaluate(
        self,
        *,
        gate_name: str,
        snapshot: ExperimentResultSnapshot,
        minimum_required_score: float,
        metric_name: str = "overall_score",
        expected_value: float | None = None,
        notes: str | None = None,
    ) -> QualityGateResult: ...


class BlockingFailureCounting(Protocol):
    def count(
        self,
        *,
        gate_results: tuple[QualityGateResult, ...],
    ) -> int: ...


class CIPolicyEvaluation(Protocol):
    def evaluate(
        self,
        *,
        blocking_failure_count: int,
    ) -> bool: ...


class CIBenchmarkPolicyResultBuilding(Protocol):
    def build(
        self,
        *,
        policy_name: str,
        snapshot: ExperimentResultSnapshot,
        minimum_required_score: float,
        gate_results: tuple[QualityGateResult, ...],
        blocking_failure_count: int,
        deployment_allowed: bool,
        notes: str | None = None,
    ) -> CIBenchmarkPolicyResult: ...
