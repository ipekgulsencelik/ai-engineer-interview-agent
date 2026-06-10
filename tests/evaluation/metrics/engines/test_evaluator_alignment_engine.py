from __future__ import annotations

import pytest

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.metrics.calculators.cohens_kappa_calculator import (
    CohensKappaCalculator,
)
from src.evaluation.metrics.calculators.pearson_correlation_calculator import (
    PearsonCorrelationCalculator,
)
from src.evaluation.metrics.calculators.regression_metrics_calculator import (
    RegressionMetricsCalculator,
)
from src.evaluation.metrics.engines.evaluator_alignment_engine import (
    EvaluatorAlignmentEngine,
)
from src.evaluation.metrics.entities.evaluator_alignment_report import (
    EvaluatorAlignmentReport,
)


def _engine() -> EvaluatorAlignmentEngine:
    return EvaluatorAlignmentEngine(
        pearson_calculator=PearsonCorrelationCalculator(),
        agreement_calculator=CohensKappaCalculator(),
        regression_calculator=RegressionMetricsCalculator(),
    )


def test_evaluator_alignment_engine_should_build_alignment_report() -> None:
    report = _engine().evaluate(
        report_id="report-1",
        evaluator_id="evaluator-1",
        model_name="gpt-5",
        human_scores=(1.0, 2.0, 3.0, 4.0),
        llm_scores=(1.0, 2.0, 3.0, 4.0),
        human_labels=("low", "medium", "medium", "high"),
        llm_labels=("low", "medium", "medium", "high"),
        notes="engine test",
    )

    assert isinstance(report, EvaluatorAlignmentReport)
    assert report.report_id == "report-1"
    assert report.evaluator_id == "evaluator-1"
    assert report.model_name == "gpt-5"
    assert report.pearson_correlation.correlation_coefficient == pytest.approx(1.0)
    assert report.agreement_result.agreement_ratio == pytest.approx(1.0)
    assert report.regression_result.r2_score == pytest.approx(1.0)
    assert report.overall_alignment_score == pytest.approx(1.0)
    assert report.notes == "engine test"


def test_evaluator_alignment_engine_should_raise_for_mismatched_scores() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="human_scores and llm_scores must have the same length",
    ):
        _engine().evaluate(
            report_id="report-1",
            evaluator_id="evaluator-1",
            model_name="gpt-5",
            human_scores=(1.0, 2.0),
            llm_scores=(1.0,),
            human_labels=("low", "high"),
            llm_labels=("low", "high"),
        )


class _FakeCorrelationCalculator:
    def calculate(
        self,
        *,
        metric_x: str,
        metric_y: str,
        x_values,
        y_values,
    ):
        from tests.evaluation.metrics.factories import correlation_result

        return correlation_result(coefficient=0.50, sample_count=len(x_values))


class _FakeAgreementCalculator:
    def calculate(
        self,
        *,
        metric_name: str,
        evaluator_a_labels,
        evaluator_b_labels,
    ):
        from tests.evaluation.metrics.factories import agreement_result

        return agreement_result(
            agreement_ratio=0.60, sample_count=len(evaluator_a_labels)
        )


class _FakeRegressionCalculator:
    def calculate(
        self,
        *,
        metric_name: str,
        actual_values,
        predicted_values,
    ):
        from tests.evaluation.metrics.factories import regression_result

        return regression_result(r2_score=0.70, sample_count=len(actual_values))


class _FakeEvaluatorAlignmentReportBuilder:
    def build(
        self,
        *,
        report_id: str,
        evaluator_id: str,
        model_name: str,
        correlation_result,
        agreement_result,
        regression_result,
        notes: str | None = None,
    ) -> EvaluatorAlignmentReport:
        return EvaluatorAlignmentReport(
            report_id=report_id,
            evaluator_id=evaluator_id,
            model_name=model_name,
            pearson_correlation=correlation_result,
            agreement_result=agreement_result,
            regression_result=regression_result,
            overall_alignment_score=0.55,
            interpretation="fake_alignment",
            notes=notes,
        )


def test_evaluator_alignment_engine_should_use_injected_dependencies() -> None:
    report = EvaluatorAlignmentEngine(
        pearson_calculator=_FakeCorrelationCalculator(),
        agreement_calculator=_FakeAgreementCalculator(),
        regression_calculator=_FakeRegressionCalculator(),
        report_builder=_FakeEvaluatorAlignmentReportBuilder(),
    ).evaluate(
        report_id="report-1",
        evaluator_id="evaluator-1",
        model_name="gpt-5",
        human_scores=(1.0, 2.0, 3.0),
        llm_scores=(1.2, 1.9, 2.8),
        human_labels=("low", "medium", "high"),
        llm_labels=("low", "medium", "high"),
        notes="injected engine test",
    )

    assert report.overall_alignment_score == pytest.approx(0.55)
    assert report.pearson_correlation.correlation_coefficient == pytest.approx(0.50)
    assert report.agreement_result.agreement_ratio == pytest.approx(0.60)
    assert report.regression_result.r2_score == pytest.approx(0.70)
    assert report.interpretation == "fake_alignment"
    assert report.notes == "injected engine test"
