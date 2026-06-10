from __future__ import annotations

from src.domain.validation.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.ops.schemas.regression_detection_result_schema import (
    REGRESSION_DETECTION_RESULT_SCHEMA,
)


class RegressionDetectionResultValidator:
    """
    RegressionDetectionResult validation service.
    """

    SCORE_DELTA_TOLERANCE = 1e-9

    @classmethod
    def validate(
        cls,
        *,
        benchmark_id: str,
        benchmark_name: str,
        benchmark_version: str,
        baseline_experiment_id: str,
        candidate_experiment_id: str,
        baseline_score: float,
        candidate_score: float,
        score_delta: float,
        regression_threshold: float,
        regression_detected: bool,
        interpretation: str,
        notes: str | None = None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "benchmark_id": benchmark_id,
                "benchmark_name": benchmark_name,
                "benchmark_version": benchmark_version,
                "baseline_experiment_id": baseline_experiment_id,
                "candidate_experiment_id": candidate_experiment_id,
                "baseline_score": baseline_score,
                "candidate_score": candidate_score,
                "score_delta": score_delta,
                "regression_threshold": regression_threshold,
                "regression_detected": regression_detected,
                "interpretation": interpretation,
                "notes": notes,
            },
            schema=REGRESSION_DETECTION_RESULT_SCHEMA,
            error_factory=EvaluationValidationError,
        )

        cls._validate_experiment_ids(
            baseline_experiment_id=baseline_experiment_id,
            candidate_experiment_id=candidate_experiment_id,
        )

        cls._validate_score_delta(
            baseline_score=baseline_score,
            candidate_score=candidate_score,
            score_delta=score_delta,
        )

    @staticmethod
    def _validate_experiment_ids(
        *,
        baseline_experiment_id: str,
        candidate_experiment_id: str,
    ) -> None:
        if baseline_experiment_id == candidate_experiment_id:
            raise EvaluationValidationError(
                "baseline_experiment_id and candidate_experiment_id must be different."
            )

    @classmethod
    def _validate_score_delta(
        cls,
        *,
        baseline_score: float,
        candidate_score: float,
        score_delta: float,
    ) -> None:
        expected_delta = (
            candidate_score
            - baseline_score
        )

        if abs(
            score_delta
            - expected_delta
        ) > cls.SCORE_DELTA_TOLERANCE:
            raise EvaluationValidationError(
                "score_delta must equal candidate_score - baseline_score."
            )