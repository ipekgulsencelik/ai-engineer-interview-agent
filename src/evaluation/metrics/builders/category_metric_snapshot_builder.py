from __future__ import annotations

from statistics import mean

from src.evaluation.metrics.builders.evaluator_alignment_report_builder import (
    EvaluatorAlignmentReportBuilder,
)
from src.evaluation.metrics.value_objects.agreement_result import (
    AgreementResult,
)
from src.evaluation.metrics.value_objects.category_metric_snapshot import (
    CategoryMetricSnapshot,
)
from src.evaluation.metrics.value_objects.correlation_result import (
    CorrelationResult,
)
from src.evaluation.metrics.value_objects.regression_metric_result import (
    RegressionMetricResult,
)


class CategoryMetricSnapshotBuilder:
    """
    Builds category-level metric snapshots.
    """

    @staticmethod
    def build(
        *,
        category: str,
        human_scores: tuple[float, ...],
        llm_scores: tuple[float, ...],
        correlation_result: CorrelationResult,
        agreement_result: AgreementResult,
        regression_result: RegressionMetricResult,
        notes: str | None = None,
    ) -> CategoryMetricSnapshot:
        alignment_report = EvaluatorAlignmentReportBuilder.build(
            report_id=f"category-{category}",
            evaluator_id="category_metrics_analyzer",
            model_name="category_metrics",
            correlation_result=correlation_result,
            agreement_result=agreement_result,
            regression_result=regression_result,
            notes=notes,
        )

        return CategoryMetricSnapshot(
            category=category,
            average_human_score=mean(human_scores),
            average_llm_score=mean(llm_scores),
            correlation_result=correlation_result,
            agreement_result=agreement_result,
            regression_result=regression_result,
            overall_alignment_score=(
                alignment_report.overall_alignment_score
            ),
            interpretation=alignment_report.interpretation,
            notes=notes,
        )