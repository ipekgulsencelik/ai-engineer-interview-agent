from __future__ import annotations

from collections.abc import Sequence

from src.evaluation.metrics.builders.evaluator_alignment_report_builder import (
    EvaluatorAlignmentReportBuilder,
)
from src.evaluation.metrics.calculators.cohen_kappa_calculator import (
    CohenKappaCalculator,
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


class EvaluatorAlignmentEngine:
    """
    High-level evaluator alignment orchestration engine.

    Coordinates correlation, agreement, and regression metrics
    without owning calculation, interpretation, or report-building logic.
    """

    def __init__(
        self,
        *,
        pearson_calculator: PearsonCorrelationCalculator,
        agreement_calculator: CohenKappaCalculator,
        regression_calculator: RegressionMetricsCalculator,
    ) -> None:
        self._pearson_calculator = pearson_calculator
        self._agreement_calculator = agreement_calculator
        self._regression_calculator = regression_calculator

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

        return EvaluatorAlignmentReportBuilder.build(
            report_id=report_id,
            evaluator_id=evaluator_id,
            model_name=model_name,
            correlation_result=correlation_result,
            agreement_result=agreement_result,
            regression_result=regression_result,
            notes=notes,
        )