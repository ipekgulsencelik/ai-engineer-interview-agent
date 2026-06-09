from __future__ import annotations

import pytest

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
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


def _correlation_result() -> CorrelationResult:
    return CorrelationResult(
        metric_x="human_score",
        metric_y="llm_score",
        correlation_coefficient=0.82,
        p_value=0.01,
        sample_count=100,
        method="pearson",
        is_significant=True,
        interpretation="strong",
    )


def _agreement_result() -> AgreementResult:
    return AgreementResult(
        metric_name="overall_label",
        kappa_score=0.78,
        agreement_ratio=0.88,
        sample_count=100,
        evaluator_count=2,
        method="cohen_kappa",
        is_reliable=True,
        interpretation="strong",
    )


def _regression_result() -> RegressionMetricResult:
    return RegressionMetricResult(
        metric_name="score_regression",
        mae=0.25,
        mse=0.125,
        rmse=0.3535,
        r2_score=0.82,
        sample_count=100,
        is_acceptable=True,
        interpretation="good",
    )


def test_evaluator_alignment_report_should_create_successfully() -> None:
    report = EvaluatorAlignmentReport(
        report_id="report-1",
        evaluator_id="evaluator-1",
        model_name="gpt-5",
        pearson_correlation=_correlation_result(),
        agreement_result=_agreement_result(),
        regression_result=_regression_result(),
        overall_alignment_score=0.82,
        interpretation="strong_alignment",
        notes="Valid alignment report.",
    )

    assert report.report_id == "report-1"
    assert report.evaluator_id == "evaluator-1"
    assert report.model_name == "gpt-5"
    assert report.overall_alignment_score == 0.82
    assert report.is_strongly_aligned is True
    assert report.is_moderately_aligned is False
    assert report.is_weakly_aligned is False


def test_evaluator_alignment_report_should_be_moderately_aligned() -> None:
    report = EvaluatorAlignmentReport(
        report_id="report-1",
        evaluator_id="evaluator-1",
        model_name="gpt-5",
        pearson_correlation=_correlation_result(),
        agreement_result=_agreement_result(),
        regression_result=_regression_result(),
        overall_alignment_score=0.70,
        interpretation="moderate_alignment",
    )

    assert report.is_strongly_aligned is False
    assert report.is_moderately_aligned is True
    assert report.is_weakly_aligned is False


def test_evaluator_alignment_report_should_be_weakly_aligned() -> None:
    report = EvaluatorAlignmentReport(
        report_id="report-1",
        evaluator_id="evaluator-1",
        model_name="gpt-5",
        pearson_correlation=_correlation_result(),
        agreement_result=_agreement_result(),
        regression_result=_regression_result(),
        overall_alignment_score=0.40,
        interpretation="weak_alignment",
    )

    assert report.is_strongly_aligned is False
    assert report.is_moderately_aligned is False
    assert report.is_weakly_aligned is True


@pytest.mark.parametrize(
    "field_name",
    [
        "report_id",
        "evaluator_id",
        "model_name",
        "interpretation",
    ],
)
def test_evaluator_alignment_report_should_raise_for_empty_string_fields(
    field_name: str,
) -> None:
    kwargs = {
        "report_id": "report-1",
        "evaluator_id": "evaluator-1",
        "model_name": "gpt-5",
        "pearson_correlation": _correlation_result(),
        "agreement_result": _agreement_result(),
        "regression_result": _regression_result(),
        "overall_alignment_score": 0.82,
        "interpretation": "strong_alignment",
        "notes": None,
    }
    kwargs[field_name] = ""

    with pytest.raises(
        EvaluationValidationError,
    ):
        EvaluatorAlignmentReport(**kwargs)


def test_evaluator_alignment_report_should_raise_for_invalid_overall_alignment_score() -> None:
    with pytest.raises(
        EvaluationValidationError,
    ):
        EvaluatorAlignmentReport(
            report_id="report-1",
            evaluator_id="evaluator-1",
            model_name="gpt-5",
            pearson_correlation=_correlation_result(),
            agreement_result=_agreement_result(),
            regression_result=_regression_result(),
            overall_alignment_score=1.5,
            interpretation="invalid",
        )


def test_evaluator_alignment_report_should_be_immutable() -> None:
    report = EvaluatorAlignmentReport(
        report_id="report-1",
        evaluator_id="evaluator-1",
        model_name="gpt-5",
        pearson_correlation=_correlation_result(),
        agreement_result=_agreement_result(),
        regression_result=_regression_result(),
        overall_alignment_score=0.82,
        interpretation="strong_alignment",
    )

    with pytest.raises(
        AttributeError,
    ):
        report.report_id = "changed"  # type: ignore[misc]