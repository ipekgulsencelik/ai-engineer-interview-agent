from __future__ import annotations

import pytest

from src.evaluation.metrics.builders.evaluator_alignment_report_builder import (
    EvaluatorAlignmentReportBuilder,
)
from src.evaluation.metrics.entities.evaluator_alignment_report import (
    EvaluatorAlignmentReport,
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


def test_evaluator_alignment_report_builder_should_build_report() -> None:
    report = EvaluatorAlignmentReportBuilder.build(
        report_id="report-1",
        evaluator_id="evaluator-1",
        model_name="gpt-5",
        correlation_result=CorrelationResult(
            metric_x="human_score",
            metric_y="llm_score",
            correlation_coefficient=0.90,
            p_value=0.01,
            sample_count=3,
            method="pearson",
            is_significant=True,
            interpretation="very_strong",
        ),
        agreement_result=AgreementResult(
            metric_name="human_llm_agreement",
            kappa_score=0.80,
            agreement_ratio=0.80,
            sample_count=3,
            evaluator_count=2,
            method="cohen_kappa",
            is_reliable=True,
            interpretation="strong",
        ),
        regression_result=RegressionMetricResult(
            metric_name="human_llm_regression",
            mae=0.10,
            mse=0.01,
            rmse=0.10,
            r2_score=0.70,
            sample_count=3,
            is_acceptable=True,
            interpretation="moderate",
        ),
        notes="Builder test.",
    )

    assert isinstance(report, EvaluatorAlignmentReport)
    assert report.report_id == "report-1"
    assert report.overall_alignment_score == pytest.approx(0.80)
    assert report.interpretation == "strong_alignment"
    assert report.notes == "Builder test."