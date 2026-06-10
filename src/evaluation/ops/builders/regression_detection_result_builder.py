from __future__ import annotations

from src.evaluation.metrics.entities.experiment_result_snapshot import (
    ExperimentResultSnapshot,
)
from src.evaluation.ops.calculators.regression_score_delta_calculator import (
    RegressionScoreDeltaCalculator,
)
from src.evaluation.ops.constants.regression_detection import (
    DEFAULT_REGRESSION_THRESHOLD,
)
from src.evaluation.ops.interpreters.regression_detection_interpreter import (
    RegressionDetectionInterpreter,
)
from src.evaluation.ops.value_objects.regression_detection_result import (
    RegressionDetectionResult,
)


class RegressionDetectionResultBuilder:
    """
    Builds RegressionDetectionResult instances.
    """

    @staticmethod
    def build(
        *,
        baseline_snapshot: ExperimentResultSnapshot,
        candidate_snapshot: ExperimentResultSnapshot,
        regression_threshold: float = DEFAULT_REGRESSION_THRESHOLD,
        notes: str | None = None,
    ) -> RegressionDetectionResult:
        score_delta = RegressionScoreDeltaCalculator.calculate(
            baseline_score=baseline_snapshot.overall_score,
            candidate_score=candidate_snapshot.overall_score,
        )

        return RegressionDetectionResult(
            benchmark_id=baseline_snapshot.benchmark_id,
            benchmark_name=baseline_snapshot.benchmark_name,
            benchmark_version=baseline_snapshot.benchmark_version,
            baseline_experiment_id=baseline_snapshot.experiment_id,
            candidate_experiment_id=candidate_snapshot.experiment_id,
            baseline_score=baseline_snapshot.overall_score,
            candidate_score=candidate_snapshot.overall_score,
            score_delta=score_delta,
            regression_threshold=regression_threshold,
            regression_detected=(
                score_delta <= -regression_threshold
            ),
            interpretation=RegressionDetectionInterpreter.interpret(
                score_delta=score_delta,
                regression_threshold=regression_threshold,
            ),
            notes=notes,
        )