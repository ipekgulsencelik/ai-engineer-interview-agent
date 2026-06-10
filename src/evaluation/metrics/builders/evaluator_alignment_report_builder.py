from __future__ import annotations

from src.evaluation.metrics.calculators.overall_alignment_score_calculator import (
    OverallAlignmentScoreCalculator,
)
from src.evaluation.metrics.entities.evaluator_alignment_report import (
    EvaluatorAlignmentReport,
)
from src.evaluation.metrics.interpreters.alignment_interpreter import (
    AlignmentInterpreter,
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


class EvaluatorAlignmentReportBuilder:
    """
    Builds EvaluatorAlignmentReport instances.
    """

    @staticmethod
    def build(
        *,
        report_id: str,
        evaluator_id: str,
        model_name: str,
        correlation_result: CorrelationResult,
        agreement_result: AgreementResult,
        regression_result: RegressionMetricResult,
        notes: str | None = None,
    ) -> EvaluatorAlignmentReport:
        overall_alignment_score = (
            OverallAlignmentScoreCalculator.calculate(
                correlation_score=abs(
                    correlation_result.correlation_coefficient,
                ),
                agreement_score=agreement_result.agreement_ratio,
                regression_score=regression_result.r2_score,
            )
        )

        return EvaluatorAlignmentReport(
            report_id=report_id,
            evaluator_id=evaluator_id,
            model_name=model_name,
            pearson_correlation=correlation_result,
            agreement_result=agreement_result,
            regression_result=regression_result,
            overall_alignment_score=overall_alignment_score,
            interpretation=AlignmentInterpreter.interpret(
                alignment_score=overall_alignment_score,
            ),
            notes=notes,
        )