from __future__ import annotations

from collections.abc import Sequence

from src.evaluation.metrics.calculators.agreement_ratio_calculator import (
    AgreementRatioCalculator,
)
from src.evaluation.metrics.calculators.cohen_kappa_score_calculator import (
    CohenKappaScoreCalculator,
)
from src.evaluation.metrics.constants.agreements import (
    COHEN_KAPPA_METHOD_NAME,
    DEFAULT_AGREEMENT_RELIABILITY_THRESHOLD,
)
from src.evaluation.metrics.interpreters.agreement_interpreter import (
    AgreementInterpreter,
)
from src.evaluation.metrics.validators.agreement_input_validator import (
    AgreementInputValidator,
)
from src.evaluation.metrics.value_objects.agreement_result import (
    AgreementResult,
)


class CohenKappaCalculator:
    """
    Cohen's kappa agreement calculator.

    Orchestrates input validation, raw agreement calculation,
    kappa score calculation, interpretation, and result assembly.
    """

    @staticmethod
    def calculate(
        *,
        metric_name: str,
        evaluator_a_labels: Sequence[str],
        evaluator_b_labels: Sequence[str],
        p_value: float | None = None,
        notes: str | None = None,
    ) -> AgreementResult:
        AgreementInputValidator.validate(
            evaluator_a_labels=evaluator_a_labels,
            evaluator_b_labels=evaluator_b_labels,
        )

        agreement_ratio = AgreementRatioCalculator.calculate(
            evaluator_a_labels=evaluator_a_labels,
            evaluator_b_labels=evaluator_b_labels,
        )

        kappa_score = CohenKappaScoreCalculator.calculate(
            evaluator_a_labels=evaluator_a_labels,
            evaluator_b_labels=evaluator_b_labels,
            agreement_ratio=agreement_ratio,
        )

        return AgreementResult(
            metric_name=metric_name,
            kappa_score=kappa_score,
            agreement_ratio=agreement_ratio,
            sample_count=len(
                evaluator_a_labels,
            ),
            evaluator_count=2,
            method=COHEN_KAPPA_METHOD_NAME,
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