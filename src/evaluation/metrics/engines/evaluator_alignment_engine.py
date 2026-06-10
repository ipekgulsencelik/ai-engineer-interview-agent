from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol

from src.evaluation.metrics.builders.evaluator_alignment_report_builder import (
    EvaluatorAlignmentReportBuilder,
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
from src.evaluation.metrics.constants.alignment import (
    HUMAN_LLM_AGREEMENT_METRIC_NAME,
    HUMAN_LLM_REGRESSION_METRIC_NAME,
    HUMAN_SCORE_METRIC_NAME,
    LLM_SCORE_METRIC_NAME,
)
from src.evaluation.metrics.entities.evaluator_alignment_report import (
    EvaluatorAlignmentReport,
)
from src.evaluation.metrics.validators.evaluator_alignment_input_validator import (
    EvaluatorAlignmentInputValidator,
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


class CorrelationCalculatorProtocol(Protocol):
    """
    Contract for evaluator alignment correlation calculators.
    """

    def calculate(
        self,
        *,
        metric_x: str,
        metric_y: str,
        x_values: Sequence[float],
        y_values: Sequence[float],
    ) -> CorrelationResult: ...


class AgreementCalculatorProtocol(Protocol):
    """
    Contract for evaluator alignment agreement calculators.
    """

    def calculate(
        self,
        *,
        metric_name: str,
        evaluator_a_labels: Sequence[str],
        evaluator_b_labels: Sequence[str],
    ) -> AgreementResult: ...


class RegressionCalculatorProtocol(Protocol):
    """
    Contract for evaluator alignment regression calculators.
    """

    def calculate(
        self,
        *,
        metric_name: str,
        actual_values: Sequence[float],
        predicted_values: Sequence[float],
    ) -> RegressionMetricResult: ...


class EvaluatorAlignmentReportBuilderProtocol(Protocol):
    """
    Contract for evaluator alignment report builders.
    """

    def build(
        self,
        *,
        report_id: str,
        evaluator_id: str,
        model_name: str,
        correlation_result: CorrelationResult,
        agreement_result: AgreementResult,
        regression_result: RegressionMetricResult,
        notes: str | None = None,
    ) -> EvaluatorAlignmentReport: ...


class EvaluatorAlignmentEngine:
    """
    High-level evaluator alignment orchestration engine.

    Coordinates correlation, agreement, and regression metrics
    without owning calculation, interpretation, or report-building logic.
    """

    def __init__(
        self,
        *,
        pearson_calculator: CorrelationCalculatorProtocol | None = None,
        agreement_calculator: AgreementCalculatorProtocol | None = None,
        regression_calculator: RegressionCalculatorProtocol | None = None,
        report_builder: EvaluatorAlignmentReportBuilderProtocol | None = None,
    ) -> None:
        self._pearson_calculator = pearson_calculator or PearsonCorrelationCalculator()
        self._agreement_calculator = agreement_calculator or CohensKappaCalculator()
        self._regression_calculator = (
            regression_calculator or RegressionMetricsCalculator()
        )
        self._report_builder = report_builder or EvaluatorAlignmentReportBuilder()

    def evaluate(
        self,
        *,
        report_id: str,
        evaluator_id: str,
        model_name: str,
        human_scores: Sequence[float],
        llm_scores: Sequence[float],
        human_labels: Sequence[str],
        llm_labels: Sequence[str],
        notes: str | None = None,
    ) -> EvaluatorAlignmentReport:
        EvaluatorAlignmentInputValidator.validate(
            human_scores=human_scores,
            llm_scores=llm_scores,
            human_labels=human_labels,
            llm_labels=llm_labels,
        )

        correlation_result = self._pearson_calculator.calculate(
            metric_x=HUMAN_SCORE_METRIC_NAME,
            metric_y=LLM_SCORE_METRIC_NAME,
            x_values=human_scores,
            y_values=llm_scores,
        )

        agreement_result = self._agreement_calculator.calculate(
            metric_name=HUMAN_LLM_AGREEMENT_METRIC_NAME,
            evaluator_a_labels=human_labels,
            evaluator_b_labels=llm_labels,
        )

        regression_result = self._regression_calculator.calculate(
            metric_name=HUMAN_LLM_REGRESSION_METRIC_NAME,
            actual_values=human_scores,
            predicted_values=llm_scores,
        )

        return self._report_builder.build(
            report_id=report_id,
            evaluator_id=evaluator_id,
            model_name=model_name,
            correlation_result=correlation_result,
            agreement_result=agreement_result,
            regression_result=regression_result,
            notes=notes,
        )
