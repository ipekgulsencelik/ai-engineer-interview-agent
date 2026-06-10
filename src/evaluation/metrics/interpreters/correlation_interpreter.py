from __future__ import annotations

from src.evaluation.metrics.constants.correlations import (
    MODERATE_CORRELATION_THRESHOLD,
    STRONG_CORRELATION_THRESHOLD,
    VERY_STRONG_CORRELATION_THRESHOLD,
    WEAK_CORRELATION_THRESHOLD,
)


class CorrelationInterpreter:
    """
    Correlation strength interpreter.
    """

    @staticmethod
    def interpret(
        *,
        correlation_coefficient: float,
    ) -> str:
        absolute = abs(
            correlation_coefficient,
        )

        if absolute >= VERY_STRONG_CORRELATION_THRESHOLD:
            return "very_strong"

        if absolute >= STRONG_CORRELATION_THRESHOLD:
            return "strong"

        if absolute >= MODERATE_CORRELATION_THRESHOLD:
            return "moderate"

        if absolute >= WEAK_CORRELATION_THRESHOLD:
            return "weak"

        return "very_weak"