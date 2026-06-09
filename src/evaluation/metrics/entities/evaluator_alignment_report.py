from __future__ import annotations

from dataclasses import dataclass

from src.evaluation.metrics.constants.alignment import (
    MODERATE_ALIGNMENT_THRESHOLD,
    STRONG_ALIGNMENT_THRESHOLD,
)
from src.evaluation.metrics.validators.evaluator_alignment_report_validator import (
    EvaluatorAlignmentReportValidator,
)
from src.evaluation.metrics.value_objects.agreement_result import (
    AgreementResult,
)
from src.evaluation.metrics.value_objects.correlation_result import (
    CorrelationResult,
)
from src.evaluation.metrics.value_objects.regression_metric_result import (
    RegressionMetricResult,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class EvaluatorAlignmentReport:
    """
    Immutable evaluator alignment report.

    Represents statistical alignment between human evaluator
    scores and model-generated evaluation scores.
    """

    report_id: str

    evaluator_id: str
    model_name: str

    pearson_correlation: CorrelationResult
    agreement_result: AgreementResult
    regression_result: RegressionMetricResult

    overall_alignment_score: float
    interpretation: str

    notes: str | None = None

    def __post_init__(
        self,
    ) -> None:
        EvaluatorAlignmentReportValidator.validate(
            report_id=self.report_id,
            evaluator_id=self.evaluator_id,
            model_name=self.model_name,
            pearson_correlation=self.pearson_correlation,
            agreement_result=self.agreement_result,
            regression_result=self.regression_result,
            overall_alignment_score=self.overall_alignment_score,
            interpretation=self.interpretation,
            notes=self.notes,
        )

    @property
    def is_strongly_aligned(
        self,
    ) -> bool:
        return (
            self.overall_alignment_score
            >= STRONG_ALIGNMENT_THRESHOLD
        )

    @property
    def is_moderately_aligned(
        self,
    ) -> bool:
        return (
            MODERATE_ALIGNMENT_THRESHOLD
            <= self.overall_alignment_score
            < STRONG_ALIGNMENT_THRESHOLD
        )

    @property
    def is_weakly_aligned(
        self,
    ) -> bool:
        return (
            self.overall_alignment_score
            < MODERATE_ALIGNMENT_THRESHOLD
        )