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
