from __future__ import annotations

from collections.abc import Sequence

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.metrics.entities.experiment_result_snapshot import (
    ExperimentResultSnapshot,
)


class TrendVisualizationInputValidator:
    """
    Trend visualization input validation service.
    """

    @staticmethod
    def validate(
        *,
        snapshots: Sequence[ExperimentResultSnapshot],
    ) -> None:
        if not snapshots:
            raise EvaluationValidationError(
                "snapshots cannot be empty."
            )

        for index, snapshot in enumerate(
            snapshots,
        ):
            if not isinstance(
                snapshot,
                ExperimentResultSnapshot,
            ):
                raise EvaluationValidationError(
                    f"snapshots[{index}] must be ExperimentResultSnapshot."
                )