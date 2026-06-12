from __future__ import annotations

import pytest

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.ops.value_objects.regression_detection_result import (
    RegressionDetectionResult,
)


def test_regression_detection_result_should_expose_score_change_helpers() -> None:
    result = RegressionDetectionResult(
        benchmark_id="benchmark-1",
        benchmark_name="AI Engineer Benchmark",
        benchmark_version="1.0.0",
        baseline_experiment_id="baseline-1",
        candidate_experiment_id="candidate-1",
        baseline_score=0.80,
        candidate_score=0.70,
        score_delta=-0.10,
        regression_threshold=0.03,
        regression_detected=True,
        interpretation="regression_detected",
        notes="Regression detected.",
    )

    assert result.absolute_score_delta == pytest.approx(0.10)
    assert result.degraded is True
    assert result.improved is False
    assert result.unchanged is False
    assert result.score_change_percentage == pytest.approx(-12.5)


def test_regression_detection_result_should_raise_for_incorrect_delta() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="score_delta must equal",
    ):
        RegressionDetectionResult(
            benchmark_id="benchmark-1",
            benchmark_name="AI Engineer Benchmark",
            benchmark_version="1.0.0",
            baseline_experiment_id="baseline-1",
            candidate_experiment_id="candidate-1",
            baseline_score=0.80,
            candidate_score=0.70,
            score_delta=-0.20,
            regression_threshold=0.03,
            regression_detected=True,
            interpretation="regression_detected",
        )
