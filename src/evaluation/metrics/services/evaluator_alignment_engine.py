from __future__ import annotations

from src.evaluation.metrics.entities import (
    EvaluatorAlignmentReport,
)
from src.evaluation.metrics.factories.evaluator_alignment_report_factory import (
    EvaluatorAlignmentReportFactory,
)
from src.evaluation.metrics.services.cohens_kappa_calculator import (
    CohensKappaCalculator,
)
from src.evaluation.metrics.services.evaluator_alignment_interpreter import (
    EvaluatorAlignmentInterpreter,
)
from src.evaluation.metrics.services.evaluator_alignment_score_calculator import (
    EvaluatorAlignmentScoreCalculator,
)
from src.evaluation.metrics.services.mae_calculator import (
    MAECalculator,
)
from src.evaluation.metrics.services.pearson_correlation_calculator import (
    PearsonCorrelationCalculator,
)
from src.evaluation.metrics.services.rmse_calculator import (
    RMSECalculator,
)


class EvaluatorAlignmentEngine:
    """
    Composite evaluator alignment analysis engine.
    """

    def __init__(
        self,
        *,
        pearson_calculator: PearsonCorrelationCalculator,
        kappa_calculator: CohensKappaCalculator,
        mae_calculator: MAECalculator,
        rmse_calculator: RMSECalculator,
        score_calculator: EvaluatorAlignmentScoreCalculator,
        interpreter: EvaluatorAlignmentInterpreter,
    ) -> None:
        self._pearson_calculator = pearson_calculator
        self._kappa_calculator = kappa_calculator
        self._mae_calculator = mae_calculator
        self._rmse_calculator = rmse_calculator
        self._score_calculator = score_calculator
        self._interpreter = interpreter

    def evaluate(
        self,
        *,
        human_scores: list[float],
        llm_scores: list[float],
        human_labels: list[str],
        llm_labels: list[str],
    ) -> EvaluatorAlignmentReport:
        pearson_result = self._pearson_calculator.calculate(
            human_scores=human_scores,
            llm_scores=llm_scores,
        )

        agreement_result = self._kappa_calculator.calculate(
            human_labels=human_labels,
            llm_labels=llm_labels,
        )

        mae_result = self._mae_calculator.calculate(
            human_scores=human_scores,
            llm_scores=llm_scores,
        )

        rmse_result = self._rmse_calculator.calculate(
            human_scores=human_scores,
            llm_scores=llm_scores,
        )

        overall_score = self._score_calculator.calculate(
            pearson=pearson_result.correlation_coefficient,
            kappa=agreement_result.kappa_score,
            mae=mae_result.metric_value,
            rmse=rmse_result.metric_value,
        )

        interpretation = self._interpreter.interpret(
            overall_score,
        )

        return EvaluatorAlignmentReportFactory.create(
            pearson_correlation=pearson_result,
            agreement_result=agreement_result,
            regression_result=rmse_result,
            overall_alignment_score=overall_score,
            interpretation=interpretation,
        )