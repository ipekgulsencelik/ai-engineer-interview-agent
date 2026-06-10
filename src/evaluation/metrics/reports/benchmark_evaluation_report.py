from __future__ import annotations

from dataclasses import dataclass

from src.evaluation.metrics.entities.evaluator_alignment_report import (
    EvaluatorAlignmentReport,
)
from src.evaluation.metrics.validators.benchmark_evaluation_report_validator import (
    BenchmarkEvaluationReportValidator,
)
from src.evaluation.metrics.value_objects.category_metric_snapshot import (
    CategoryMetricSnapshot,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class BenchmarkEvaluationReport:
    """
    Immutable benchmark evaluation report.

    Represents benchmark-level evaluation summary containing
    global alignment metrics and category-level snapshots.
    """

    benchmark_id: str
    benchmark_name: str

    dataset_id: str
    dataset_version: str

    model_name: str
    evaluator_id: str

    alignment_report: EvaluatorAlignmentReport
    category_snapshots: tuple[CategoryMetricSnapshot, ...]

    overall_score: float
    interpretation: str

    notes: str | None = None

    def __post_init__(
        self,
    ) -> None:
        BenchmarkEvaluationReportValidator.validate(
            benchmark_id=self.benchmark_id,
            benchmark_name=self.benchmark_name,
            dataset_id=self.dataset_id,
            dataset_version=self.dataset_version,
            model_name=self.model_name,
            evaluator_id=self.evaluator_id,
            alignment_report=self.alignment_report,
            category_snapshots=self.category_snapshots,
            overall_score=self.overall_score,
            interpretation=self.interpretation,
            notes=self.notes,
        )

    @property
    def category_count(
        self,
    ) -> int:
        return len(
            self.category_snapshots,
        )

    @property
    def sample_count(
        self,
    ) -> int:
        return sum(snapshot.sample_count for snapshot in self.category_snapshots)

    @property
    def strongest_category(
        self,
    ) -> CategoryMetricSnapshot | None:
        if not self.category_snapshots:
            return None

        return max(
            self.category_snapshots,
            key=lambda snapshot: snapshot.overall_alignment_score,
        )

    @property
    def weakest_category(
        self,
    ) -> CategoryMetricSnapshot | None:
        if not self.category_snapshots:
            return None

        return min(
            self.category_snapshots,
            key=lambda snapshot: snapshot.overall_alignment_score,
        )

    @property
    def average_category_score(
        self,
    ) -> float:
        if not self.category_snapshots:
            return 0.0

        return sum(
            snapshot.overall_alignment_score for snapshot in self.category_snapshots
        ) / len(
            self.category_snapshots,
        )
