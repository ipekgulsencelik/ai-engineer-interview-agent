from __future__ import annotations

from src.evaluation.metrics.constants.regression_metrics import (
    EXCELLENT_R2_THRESHOLD,
    GOOD_R2_THRESHOLD,
    MODERATE_R2_THRESHOLD,
)


class RegressionMetricInterpreter:
    """
    Regression metric interpretation service.
    """

    @staticmethod
    def interpret(
        *,
        r2_score: float,
    ) -> str:
        if r2_score >= EXCELLENT_R2_THRESHOLD:
            return "excellent"

        if r2_score >= GOOD_R2_THRESHOLD:
            return "good"

        if r2_score >= MODERATE_R2_THRESHOLD:
            return "moderate"

        return "poor"