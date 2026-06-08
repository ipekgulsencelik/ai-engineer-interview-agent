from __future__ import annotations

import math

from src.evaluation.dataset.value_objects.dataset_distribution_snapshot import DatasetDistributionSnapshot
from src.evaluation.domain.errors.evaluation_validation_error import EvaluationValidationError


class DatasetDriftInputValidator:
    """Dataset drift analyzer input validation service."""

    @staticmethod
    def validate(
        *,
        baseline: DatasetDistributionSnapshot,
        comparison: DatasetDistributionSnapshot,
        drift_threshold: float,
    ) -> None:
        if not isinstance(baseline, DatasetDistributionSnapshot):
            raise EvaluationValidationError(
                "baseline must be a DatasetDistributionSnapshot."
            )
        if not isinstance(comparison, DatasetDistributionSnapshot):
            raise EvaluationValidationError(
                "comparison must be a DatasetDistributionSnapshot."
            )
        if isinstance(drift_threshold, bool) or not isinstance(drift_threshold, (int, float)):
            raise EvaluationValidationError("drift_threshold must be numeric.")
        if not math.isfinite(float(drift_threshold)):
            raise EvaluationValidationError("drift_threshold must be finite.")
        if float(drift_threshold) < 0 or float(drift_threshold) > 1:
            raise EvaluationValidationError(
                "drift_threshold must be between 0 and 1."
            )
