from __future__ import annotations

import pytest

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.ops.engines.regression_detection_engine import (
    RegressionDetectionEngine,
)
from tests.evaluation.ops.factories import experiment_snapshot


def test_regression_detection_engine_should_detect_regression() -> None:
    result = RegressionDetectionEngine.detect(
        baseline_snapshot=experiment_snapshot(
            experiment_id="baseline-1",
            overall_score=0.90,
        ),
        candidate_snapshot=experiment_snapshot(
            experiment_id="candidate-1",
            overall_score=0.85,
        ),
        regression_threshold=0.03,
    )

    assert result.regression_detected is True
    assert result.score_delta == pytest.approx(-0.05)


def test_regression_detection_engine_should_require_same_benchmark() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="same benchmark_id",
    ):
        RegressionDetectionEngine.detect(
            baseline_snapshot=experiment_snapshot(
                experiment_id="baseline-1",
                benchmark_id="benchmark-1",
            ),
            candidate_snapshot=experiment_snapshot(
                experiment_id="candidate-1",
                benchmark_id="benchmark-2",
            ),
        )
