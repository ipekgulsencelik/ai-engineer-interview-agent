from __future__ import annotations

from src.evaluation.ops.constants.quality_gates import (
    QUALITY_GATE_CRITICAL_SEVERITY,
    QUALITY_GATE_INFO_SEVERITY,
)


class QualityGateSeverityResolver:
    """
    Resolves quality gate severity.
    """

    @staticmethod
    def resolve(
        *,
        passed: bool,
    ) -> str:
        if passed:
            return (
                QUALITY_GATE_INFO_SEVERITY
            )

        return (
            QUALITY_GATE_CRITICAL_SEVERITY
        )