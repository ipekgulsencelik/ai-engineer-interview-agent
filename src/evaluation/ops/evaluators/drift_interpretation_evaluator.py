from __future__ import annotations


class DriftInterpretationEvaluator:
    """
    Evaluates drift interpretation labels.
    """

    @staticmethod
    def evaluate(
        *,
        drift_delta: float,
        alert_triggered: bool,
    ) -> str:
        if not alert_triggered:
            return "drift_within_threshold"

        if drift_delta < 0:
            return "negative_drift_detected"

        if drift_delta > 0:
            return "positive_drift_detected"

        return "no_drift_detected"