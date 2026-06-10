from __future__ import annotations

from src.evaluation.ops.constants.regression_detection import (
    IMPROVEMENT_DETECTED_INTERPRETATION,
    NO_REGRESSION_INTERPRETATION,
    REGRESSION_DETECTED_INTERPRETATION,
)


class RegressionDetectionInterpreter:
    """
    Interprets regression detection result.
    """

    @staticmethod
    def interpret(
        *,
        score_delta: float,
        regression_threshold: float,
    ) -> str:
        if score_delta <= -regression_threshold:
            return REGRESSION_DETECTED_INTERPRETATION

        if score_delta > 0:
            return IMPROVEMENT_DETECTED_INTERPRETATION

        return NO_REGRESSION_INTERPRETATION