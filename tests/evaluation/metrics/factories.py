from __future__ import annotations

from src.evaluation.metrics.value_objects.agreement_result import (
    AgreementResult,
)
from src.evaluation.metrics.value_objects.correlation_result import (
    CorrelationResult,
)
from src.evaluation.metrics.value_objects.regression_metric_result import (
    RegressionMetricResult,
)


def correlation_result(
    *,
    coefficient: float = 0.90,
    sample_count: int = 4,
) -> CorrelationResult:
    return CorrelationResult(
        metric_x="human_score",
        metric_y="llm_score",
        correlation_coefficient=coefficient,
        p_value=0.01,
        sample_count=sample_count,
        method="pearson",
        is_significant=True,
        interpretation="very_strong",
    )


def agreement_result(
    *,
    kappa_score: float = 0.80,
    agreement_ratio: float = 0.80,
    sample_count: int = 4,
) -> AgreementResult:
    return AgreementResult(
        metric_name="human_llm_agreement",
        kappa_score=kappa_score,
        agreement_ratio=agreement_ratio,
        sample_count=sample_count,
        evaluator_count=2,
        method="cohen_kappa",
        is_reliable=True,
        interpretation="strong",
    )


def regression_result(
    *,
    r2_score: float = 0.70,
    sample_count: int = 4,
) -> RegressionMetricResult:
    return RegressionMetricResult(
        metric_name="human_llm_regression",
        mae=0.10,
        mse=0.01,
        rmse=0.10,
        r2_score=r2_score,
        sample_count=sample_count,
        is_acceptable=True,
        interpretation="moderate",
    )
