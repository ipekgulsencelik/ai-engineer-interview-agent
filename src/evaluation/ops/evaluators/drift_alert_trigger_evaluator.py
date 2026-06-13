from __future__ import annotations


class DriftAlertTriggerEvaluator:
    """
    Evaluates whether drift alert should be triggered.
    """

    @staticmethod
    def evaluate(
        *,
        drift_delta: float,
        drift_threshold: float,
    ) -> bool:
        return (
            abs(drift_delta)
            >= drift_threshold
        )