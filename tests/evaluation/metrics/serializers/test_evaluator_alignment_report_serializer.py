from __future__ import annotations

from src.evaluation.metrics.entities.evaluator_alignment_report import (
    EvaluatorAlignmentReport,
)
from src.evaluation.metrics.serializers.evaluator_alignment_report_serializer import (
    EvaluatorAlignmentReportSerializer,
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


def test_evaluator_alignment_report_serializer_should_serialize_report() -> None:
    report = EvaluatorAlignmentReport(
        report_id="report-1",
        evaluator_id="evaluator-1",
        model_name="gpt-5",
        pearson_correlation=CorrelationResult(
            metric_x="human_score",
            metric_y="llm_score",
            correlation_coefficient=0.82,
            p_value=0.01,
            sample_count=100,
            method="pearson",
            is_significant=True,
            interpretation="strong",
        ),
        agreement_result=AgreementResult(
            metric_name="overall_label",
            kappa_score=0.78,
            agreement_ratio=0.88,
            sample_count=100,
            evaluator_count=2,
            method="cohen_kappa",
            is_reliable=True,
            interpretation="strong",
        ),
        regression_result=RegressionMetricResult(
            metric_name="score_regression",
            mae=0.25,
            mse=0.125,
            rmse=0.3535,
            r2_score=0.82,
            sample_count=100,
            is_acceptable=True,
            interpretation="good",
        ),
        overall_alignment_score=0.82,
        interpretation="strong_alignment",
        notes="Valid alignment report.",
    )

    payload = EvaluatorAlignmentReportSerializer.serialize(
        report=report,
    )

    assert payload["report_id"] == "report-1"
    assert payload["evaluator_id"] == "evaluator-1"
    assert payload["model_name"] == "gpt-5"
    assert payload["overall_alignment_score"] == 0.82
    assert payload["is_strongly_aligned"] is True
    assert payload["pearson_correlation"]["method"] == "pearson"
    assert payload["agreement_result"]["method"] == "cohen_kappa"
    assert payload["regression_result"]["r2_score"] == 0.82