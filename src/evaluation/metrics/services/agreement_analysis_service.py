from __future__ import annotations

from collections.abc import Sequence

from src.evaluation.metrics.calculators.cohens_kappa_calculator import (
    CohensKappaCalculator,
)
from src.evaluation.metrics.value_objects.agreement_result import (
    AgreementResult,
)


class AgreementAnalysisService:
    """
    Agreement analytics facade.

    Provides a unified entry point for evaluator
    agreement analysis workflows.
    """

    def __init__(
        self,
        *,
        cohen_kappa_calculator: (
            CohensKappaCalculator | None
        ) = None,
    ) -> None:
        self._cohen_kappa_calculator = (
            cohen_kappa_calculator
            or CohensKappaCalculator()
        )

    def analyze_cohen_kappa(
        self,
        *,
        metric_name: str,
        evaluator_a_labels: Sequence[str],
        evaluator_b_labels: Sequence[str],
        p_value: float | None = None,
        notes: str | None = None,
    ) -> AgreementResult:
        return self._cohen_kappa_calculator.calculate(
            metric_name=metric_name,
            evaluator_a_labels=evaluator_a_labels,
            evaluator_b_labels=evaluator_b_labels,
            p_value=p_value,
            notes=notes,
        )