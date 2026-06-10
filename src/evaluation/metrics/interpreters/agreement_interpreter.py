from __future__ import annotations

from src.evaluation.metrics.constants.agreements import (
    MODERATE_AGREEMENT_THRESHOLD,
    STRONG_AGREEMENT_THRESHOLD,
    VERY_STRONG_AGREEMENT_THRESHOLD,
    WEAK_AGREEMENT_THRESHOLD,
)


class AgreementInterpreter:
    """
    Agreement strength interpreter.
    """

    @staticmethod
    def interpret(
        *,
        kappa_score: float,
    ) -> str:
        absolute = abs(
            kappa_score,
        )

        if absolute >= VERY_STRONG_AGREEMENT_THRESHOLD:
            return "very_strong"

        if absolute >= STRONG_AGREEMENT_THRESHOLD:
            return "strong"

        if absolute >= MODERATE_AGREEMENT_THRESHOLD:
            return "moderate"

        if absolute >= WEAK_AGREEMENT_THRESHOLD:
            return "weak"

        return "very_weak"