from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from src.evaluation.metrics.reports.benchmark_evaluation_report import (
    BenchmarkEvaluationReport,
)
from src.evaluation.metrics.validators.experiment_result_snapshot_validator import (
    ExperimentResultSnapshotValidator,
)
from src.evaluation.metrics.value_objects.category_metric_snapshot import (
    CategoryMetricSnapshot,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ExperimentResultSnapshot:
    """
    Immutable experiment result snapshot.

    Represents a single benchmark execution result
    used for experiment tracking, leaderboard generation,
    regression detection, trend analysis, and auditability.
    """

    experiment_id: str

    benchmark_id: str
    benchmark_version: str

    dataset_id: str
    dataset_version: str
    dataset_hash: str

    model_name: str

    metrics_version: str

    benchmark_report: BenchmarkEvaluationReport

    execution_time_seconds: float

    created_at: datetime

    tags: tuple[str, ...] = ()

    notes: str | None = None

    def __post_init__(
        self,
    ) -> None:
        ExperimentResultSnapshotValidator.validate(
            experiment_id=self.experiment_id,
            benchmark_id=self.benchmark_id,
            benchmark_version=self.benchmark_version,
            dataset_id=self.dataset_id,
            dataset_version=self.dataset_version,
            dataset_hash=self.dataset_hash,
            model_name=self.model_name,
            metrics_version=self.metrics_version,
            benchmark_report=self.benchmark_report,
            execution_time_seconds=self.execution_time_seconds,
            created_at=self.created_at,
            tags=self.tags,
            notes=self.notes,
        )

    @property
    def overall_score(
        self,
    ) -> float:
        return (
            self.benchmark_report
            .overall_score
        )

    @property
    def interpretation(
        self,
    ) -> str:
        return (
            self.benchmark_report
            .interpretation
        )

    @property
    def category_count(
        self,
    ) -> int:
        return (
            self.benchmark_report
            .category_count
        )

    @property
    def sample_count(
        self,
    ) -> int:
        return (
            self.benchmark_report
            .sample_count
        )

    @property
    def strongest_category(
        self,
    ) -> CategoryMetricSnapshot | None:
        return (
            self.benchmark_report
            .strongest_category
        )

    @property
    def weakest_category(
        self,
    ) -> CategoryMetricSnapshot | None:
        return (
            self.benchmark_report
            .weakest_category
        )

    @property
    def benchmark_name(
        self,
    ) -> str:
        return (
            self.benchmark_report
            .benchmark_name
        )

    @property
    def benchmark_score(
        self,
    ) -> float:
        return (
            self.benchmark_report
            .overall_score
        )