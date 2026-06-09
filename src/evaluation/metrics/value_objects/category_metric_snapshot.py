from __future__ import annotations

from dataclasses import dataclass

from src.evaluation.metrics.validators.category_metric_snapshot_validator import (
    CategoryMetricSnapshotValidator,
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
class CategoryMetricSnapshot:
    """
    Immutable category-level evaluation metric snapshot.

    Represents evaluation quality metrics for a single
    category such as RAG, Agents, MLOps, or System Design.
    """

    category: str

    average_human_score: float
    average_llm_score: float

    correlation_result: CorrelationResult
    agreement_result: AgreementResult
    regression_result: RegressionMetricResult

    overall_alignment_score: float

    interpretation: str

    notes: str | None = None

    def __post_init__(
        self,
    ) -> None:
        CategoryMetricSnapshotValidator.validate(
            category=self.category,
            average_human_score=self.average_human_score,
            average_llm_score=self.average_llm_score,
            correlation_result=self.correlation_result,
            agreement_result=self.agreement_result,
            regression_result=self.regression_result,
            overall_alignment_score=self.overall_alignment_score,
            interpretation=self.interpretation,
            notes=self.notes,
        )

    @property
    def sample_count(
        self,
    ) -> int:
        return (
            self.correlation_result
            .sample_count
        )

    @property
    def score_delta(
        self,
    ) -> float:
        return (
            self.average_llm_score
            - self.average_human_score
        )

    @property
    def absolute_score_delta(
        self,
    ) -> float:
        return abs(
            self.score_delta,
        )

    @property
    def pearson_correlation(
        self,
    ) -> float:
        return (
            self.correlation_result
            .correlation_coefficient
        )

    @property
    def kappa_score(
        self,
    ) -> float:
        return (
            self.agreement_result
            .kappa_score
        )

    @property
    def agreement_ratio(
        self,
    ) -> float:
        return (
            self.agreement_result
            .agreement_ratio
        )

    @property
    def mae(
        self,
    ) -> float:
        return (
            self.regression_result
            .mae
        )

    @property
    def mse(
        self,
    ) -> float:
        return (
            self.regression_result
            .mse
        )

    @property
    def rmse(
        self,
    ) -> float:
        return (
            self.regression_result
            .rmse
        )

    @property
    def r2_score(
        self,
    ) -> float:
        return (
            self.regression_result
            .r2_score
        )

    @property
    def has_positive_bias(
        self,
    ) -> bool:
        return self.score_delta > 0

    @property
    def has_negative_bias(
        self,
    ) -> bool:
        return self.score_delta < 0

    @property
    def is_neutral_bias(
        self,
    ) -> bool:
        return self.score_delta == 0