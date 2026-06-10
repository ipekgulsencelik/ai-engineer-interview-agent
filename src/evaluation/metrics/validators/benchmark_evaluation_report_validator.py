from __future__ import annotations

from src.domain.validation.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.metrics.entities.evaluator_alignment_report import (
    EvaluatorAlignmentReport,
)
from src.evaluation.metrics.schemas.benchmark_evaluation_report_schema import (
    BENCHMARK_EVALUATION_REPORT_SCHEMA,
)
from src.evaluation.metrics.value_objects.category_metric_snapshot import (
    CategoryMetricSnapshot,
)


class BenchmarkEvaluationReportValidator:
    """
    BenchmarkEvaluationReport validation service.
    """

    @staticmethod
    def validate(
        *,
        benchmark_id: str,
        benchmark_name: str,
        dataset_id: str,
        dataset_version: str,
        model_name: str,
        evaluator_id: str,
        alignment_report: EvaluatorAlignmentReport,
        category_snapshots: tuple[CategoryMetricSnapshot, ...],
        overall_score: float,
        interpretation: str,
        notes: str | None = None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "benchmark_id": benchmark_id,
                "benchmark_name": benchmark_name,
                "dataset_id": dataset_id,
                "dataset_version": dataset_version,
                "model_name": model_name,
                "evaluator_id": evaluator_id,
                "overall_score": overall_score,
                "interpretation": interpretation,
                "notes": notes,
            },
            schema=BENCHMARK_EVALUATION_REPORT_SCHEMA,
            error_factory=EvaluationValidationError,
        )

        if not isinstance(
            alignment_report,
            EvaluatorAlignmentReport,
        ):
            raise EvaluationValidationError(
                "alignment_report must be EvaluatorAlignmentReport."
            )

        if not isinstance(
            category_snapshots,
            tuple,
        ):
            raise EvaluationValidationError(
                "category_snapshots must be tuple."
            )

        for index, snapshot in enumerate(
            category_snapshots,
        ):
            if not isinstance(
                snapshot,
                CategoryMetricSnapshot,
            ):
                raise EvaluationValidationError(
                    "category_snapshots"
                    f"[{index}] must be CategoryMetricSnapshot."
                )