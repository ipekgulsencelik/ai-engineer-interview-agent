from __future__ import annotations

import pytest

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.ops.validators.regression_detection_result_validator import (
    RegressionDetectionResultValidator,
)


def test_regression_detection_result_validator_should_accept_valid_result() -> None:
    RegressionDetectionResultValidator.validate(
        benchmark_id="benchmark-1",
        benchmark_name="AI Engineer Benchmark",
        benchmark_version="1.0.0",
        baseline_experiment_id="baseline-1",
        candidate_experiment_id="candidate-1",
        baseline_score=0.80,
        candidate_score=0.85,
        score_delta=0.05,
        regression_threshold=0.03,
        regression_detected=False,
        interpretation="improvement_detected",
    )


def test_regression_detection_result_validator_should_raise_for_same_experiment_ids() -> None:
    with pytest.raises(EvaluationValidationError, match="must be different"):
        RegressionDetectionResultValidator.validate(
            benchmark_id="benchmark-1",
            benchmark_name="AI Engineer Benchmark",
            benchmark_version="1.0.0",
            baseline_experiment_id="same",
            candidate_experiment_id="same",
            baseline_score=0.80,
            candidate_score=0.85,
            score_delta=0.05,
            regression_threshold=0.03,
            regression_detected=False,
            interpretation="improvement_detected",
        )
