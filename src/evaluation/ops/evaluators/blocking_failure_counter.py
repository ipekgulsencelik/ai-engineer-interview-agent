from __future__ import annotations

from src.evaluation.ops.constants.quality_gates import (
    QUALITY_GATE_CRITICAL_SEVERITY,
)
from src.evaluation.ops.value_objects.quality_gate_result import (
    QualityGateResult,
)


class BlockingFailureCounter:
    """
    Counts blocking gate failures.
    """

    @staticmethod
    def count(
        *,
        gate_results: tuple[
            QualityGateResult,
            ...,
        ],
    ) -> int:
        return sum(
            (
                not gate.passed
                and gate.severity
                == QUALITY_GATE_CRITICAL_SEVERITY
            )
            for gate in gate_results
        )