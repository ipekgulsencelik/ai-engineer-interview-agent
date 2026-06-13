from __future__ import annotations

from src.evaluation.ops.enums.drift_severity import (
    DriftSeverity,
)


class DriftSeverityEvaluator:
    """
    Evaluates drift severity.
    """

    @staticmethod
    def evaluate(
        *,
        drift_delta: float,
        drift_threshold: float,
    ) -> DriftSeverity:
        magnitude = abs(
            drift_delta,
        )

        if magnitude < drift_threshold:
            return DriftSeverity.INFO

        if magnitude >= (
            drift_threshold * 2
        ):
            return DriftSeverity.CRITICAL

        return DriftSeverity.WARNING