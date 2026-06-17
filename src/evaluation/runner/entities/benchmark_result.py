from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from src.evaluation.runner.validators.benchmark_result_validator import (
    BenchmarkResultValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class BenchmarkResult:
    """
    Immutable benchmark result.

    Represents the aggregate outcome of a benchmark
    execution and optional comparison against a
    baseline benchmark run.
    """

    result_id: str

    benchmark_id: str

    benchmark_name: str

    benchmark_version: str

    run_id: str

    experiment_id: str

    model_name: str

    started_at: datetime

    completed_at: datetime

    overall_score: float

    passed: bool

    sample_count: int

    passed_count: int

    failed_count: int

    duration_ms: float | None = None

    pass_rate: float | None = None

    average_score: float | None = None

    best_score: float | None = None

    worst_score: float | None = None

    evaluator_name: str | None = None

    dataset_id: str | None = None

    dataset_name: str | None = None

    dataset_version: str | None = None

    tenant_id: str | None = None

    baseline_run_id: str | None = None

    candidate_run_id: str | None = None

    score_delta: float | None = None

    winner: str | None = None

    error_message: str | None = None

    metadata: dict[
        str,
        str,
    ] | None = None

    def __post_init__(
        self,
    ) -> None:
        BenchmarkResultValidator.validate(
            result_id=self.result_id,
            benchmark_id=self.benchmark_id,
            benchmark_name=self.benchmark_name,
            benchmark_version=self.benchmark_version,
            run_id=self.run_id,
            experiment_id=self.experiment_id,
            model_name=self.model_name,
            started_at=self.started_at,
            completed_at=self.completed_at,
            overall_score=self.overall_score,
            passed=self.passed,
            sample_count=self.sample_count,
            passed_count=self.passed_count,
            failed_count=self.failed_count,
            duration_ms=self.duration_ms,
            pass_rate=self.pass_rate,
            average_score=self.average_score,
            best_score=self.best_score,
            worst_score=self.worst_score,
            evaluator_name=self.evaluator_name,
            dataset_id=self.dataset_id,
            dataset_name=self.dataset_name,
            dataset_version=self.dataset_version,
            tenant_id=self.tenant_id,
            baseline_run_id=self.baseline_run_id,
            candidate_run_id=self.candidate_run_id,
            score_delta=self.score_delta,
            winner=self.winner,
            error_message=self.error_message,
            metadata=self.metadata,
        )

    @property
    def has_duration(
        self,
    ) -> bool:
        return self.duration_ms is not None

    @property
    def has_comparison(
        self,
    ) -> bool:
        return (
            self.baseline_run_id is not None
            and self.candidate_run_id is not None
        )

    @property
    def has_score_delta(
        self,
    ) -> bool:
        return self.score_delta is not None

    @property
    def has_winner(
        self,
    ) -> bool:
        return self.winner is not None

    @property
    def is_regression(
        self,
    ) -> bool:
        return (
            self.score_delta is not None
            and self.score_delta < 0
        )

    @property
    def is_improvement(
        self,
    ) -> bool:
        return (
            self.score_delta is not None
            and self.score_delta > 0
        )

    @property
    def calculated_pass_rate(
        self,
    ) -> float:
        if self.sample_count == 0:
            return 0.0

        return (
            self.passed_count
            / self.sample_count
        )

    @property
    def failure_rate(
        self,
    ) -> float:
        if self.sample_count == 0:
            return 0.0

        return (
            self.failed_count
            / self.sample_count
        )

    @property
    def comparison_summary(
        self,
    ) -> str | None:
        if not self.has_comparison:
            return None

        return (
            f"{self.baseline_run_id} -> "
            f"{self.candidate_run_id} "
            f"(delta={self.score_delta})"
        )