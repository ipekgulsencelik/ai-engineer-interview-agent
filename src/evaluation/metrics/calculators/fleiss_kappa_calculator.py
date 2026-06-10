from __future__ import annotations

from collections.abc import Sequence

from src.evaluation.metrics.calculators.fleiss_agreement_ratio_calculator import (
    FleissAgreementRatioCalculator,
)
from src.evaluation.metrics.calculators.fleiss_kappa_score_calculator import (
    FleissKappaScoreCalculator,
)
from src.evaluation.metrics.constants.agreements import (
    DEFAULT_AGREEMENT_RELIABILITY_THRESHOLD,
    FLEISS_KAPPA_METHOD_NAME,
)
from src.evaluation.metrics.interpreters.agreement_interpreter import (
    AgreementInterpreter,
)
from src.evaluation.metrics.validators.fleiss_kappa_input_validator import (
    FleissKappaInputValidator,
)
from src.evaluation.metrics.value_objects.agreement_result import (
    AgreementResult,
)


class FleissKappaCalculator:
    """
    Fleiss kappa agreement calculator.

    Supports agreement analysis for two or more evaluators.
    """

    @staticmethod
    def calculate(
        *,
        metric_name: str,
        label_matrix: Sequence[Sequence[str]],
        p_value: float | None = None,
        notes: str | None = None,
    ) -> AgreementResult:
        FleissKappaInputValidator.validate(
            label_matrix=label_matrix,
        )

        agreement_ratio = FleissAgreementRatioCalculator.calculate(
            label_matrix=label_matrix,
        )

        kappa_score = FleissKappaScoreCalculator.calculate(
            label_matrix=label_matrix,
            agreement_ratio=agreement_ratio,
        )

        return AgreementResult(
            metric_name=metric_name,
            kappa_score=kappa_score,
            agreement_ratio=agreement_ratio,
            sample_count=len(label_matrix),
            evaluator_count=len(
                label_matrix[0],
            ),
            method=FLEISS_KAPPA_METHOD_NAME,
            is_reliable=(
                kappa_score
                >= DEFAULT_AGREEMENT_RELIABILITY_THRESHOLD
            ),
            interpretation=AgreementInterpreter.interpret(
                kappa_score=kappa_score,
            ),
            p_value=p_value,
            notes=notes,
        )