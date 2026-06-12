from __future__ import annotations

from collections.abc import Sequence

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.metrics.entities.experiment_result_snapshot import (
    ExperimentResultSnapshot,
)
from src.evaluation.ops.value_objects.quality_gate_result import (
    QualityGateResult,
)


class CIBenchmarkPolicyInputValidator:
    """
    CI policy input validation.
    """

    @staticmethod
    def validate(
        *,
        snapshot: ExperimentResultSnapshot,
        additional_gate_results: Sequence[
            QualityGateResult
        ],
    ) -> None:
        if not isinstance(
            snapshot,
            ExperimentResultSnapshot,
        ):
            raise EvaluationValidationError(
                "snapshot must be ExperimentResultSnapshot."
            )

        for index, gate in enumerate(
            additional_gate_results,
        ):
            if not isinstance(
                gate,
                QualityGateResult,
            ):
                raise EvaluationValidationError(
                    f"additional_gate_results[{index}] "
                    "must be QualityGateResult."
                )