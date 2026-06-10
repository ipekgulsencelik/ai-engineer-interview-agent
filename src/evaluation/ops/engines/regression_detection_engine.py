from __future__ import annotations

from src.evaluation.metrics.entities.experiment_result_snapshot import (
    ExperimentResultSnapshot,
)
from src.evaluation.ops.builders.regression_detection_result_builder import (
    RegressionDetectionResultBuilder,
)
from src.evaluation.ops.constants.regression_detection import (
    DEFAULT_REGRESSION_THRESHOLD,
)
from src.evaluation.ops.validators.regression_detection_input_validator import (
    RegressionDetectionInputValidator,
)
from src.evaluation.ops.value_objects.regression_detection_result import (
    RegressionDetectionResult,
)


class RegressionDetectionEngine:
    """
    Regression detection orchestration engine.
    """

    @staticmethod
    def detect(
        *,
        baseline_snapshot: ExperimentResultSnapshot,
        candidate_snapshot: ExperimentResultSnapshot,
        regression_threshold: float = DEFAULT_REGRESSION_THRESHOLD,
        notes: str | None = None,
    ) -> RegressionDetectionResult:
        RegressionDetectionInputValidator.validate(
            baseline_snapshot=baseline_snapshot,
            candidate_snapshot=candidate_snapshot,
            regression_threshold=regression_threshold,
        )

        return RegressionDetectionResultBuilder.build(
            baseline_snapshot=baseline_snapshot,
            candidate_snapshot=candidate_snapshot,
            regression_threshold=regression_threshold,
            notes=notes,
        )