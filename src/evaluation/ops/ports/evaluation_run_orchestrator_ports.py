from __future__ import annotations

from datetime import datetime
from typing import Protocol

from src.evaluation.metrics.entities.experiment_result_snapshot import (
    ExperimentResultSnapshot,
)
from src.evaluation.ops.value_objects.ci_benchmark_policy_result import (
    CIBenchmarkPolicyResult,
)
from src.evaluation.ops.value_objects.evaluation_run_result import EvaluationRunResult


class CIBenchmarkPolicyEvaluation(Protocol):
    def evaluate(
        self,
        *,
        policy_name: str,
        snapshot: ExperimentResultSnapshot,
        minimum_required_score: float,
        notes: str | None = None,
    ) -> CIBenchmarkPolicyResult: ...


class RunIdGeneration(Protocol):
    def generate(self) -> str: ...


class CurrentTimeProviding(Protocol):
    def now(self) -> datetime: ...


class RunDurationCalculation(Protocol):
    def calculate(
        self,
        *,
        started_at: datetime,
        completed_at: datetime,
    ) -> float: ...


class RunSuccessEvaluation(Protocol):
    def evaluate(
        self,
        *,
        ci_policy_result: CIBenchmarkPolicyResult | None,
    ) -> bool: ...


class EvaluationRunResultBuilding(Protocol):
    def build(
        self,
        *,
        run_id: str,
        snapshot: ExperimentResultSnapshot,
        started_at: datetime,
        completed_at: datetime,
        duration_seconds: float,
        success: bool,
        ci_policy_result: CIBenchmarkPolicyResult | None,
        notes: str | None = None,
    ) -> EvaluationRunResult: ...
