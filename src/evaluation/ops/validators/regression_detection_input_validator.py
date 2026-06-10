from __future__ import annotations

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.metrics.entities.experiment_result_snapshot import (
    ExperimentResultSnapshot,
)


class RegressionDetectionInputValidator:
    """
    Regression detection input validation service.
    """

    @staticmethod
    def validate(
        *,
        baseline_snapshot: ExperimentResultSnapshot,
        candidate_snapshot: ExperimentResultSnapshot,
        regression_threshold: float,
    ) -> None:
        if not isinstance(
            baseline_snapshot,
            ExperimentResultSnapshot,
        ):
            raise EvaluationValidationError(
                "baseline_snapshot must be ExperimentResultSnapshot."
            )

        if not isinstance(
            candidate_snapshot,
            ExperimentResultSnapshot,
        ):
            raise EvaluationValidationError(
                "candidate_snapshot must be ExperimentResultSnapshot."
            )

        if (
            baseline_snapshot.experiment_id
            == candidate_snapshot.experiment_id
        ):
            raise EvaluationValidationError(
                "baseline_snapshot and candidate_snapshot must be different."
            )

        if baseline_snapshot.benchmark_id != candidate_snapshot.benchmark_id:
            raise EvaluationValidationError(
                "baseline_snapshot and candidate_snapshot must have the same benchmark_id."
            )

        if (
            baseline_snapshot.benchmark_version
            != candidate_snapshot.benchmark_version
        ):
            raise EvaluationValidationError(
                "baseline_snapshot and candidate_snapshot must have the same benchmark_version."
            )

        if regression_threshold < 0:
            raise EvaluationValidationError(
                "regression_threshold cannot be negative."
            )