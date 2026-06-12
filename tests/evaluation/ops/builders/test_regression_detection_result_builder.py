from __future__ import annotations

import pytest

from src.evaluation.ops.builders.regression_detection_result_builder import (
    RegressionDetectionResultBuilder,
)
from tests.evaluation.ops.factories import experiment_snapshot


def test_regression_detection_result_builder_should_build_regression_result() -> None:
    result = RegressionDetectionResultBuilder.build(
        baseline_snapshot=experiment_snapshot(
            experiment_id="baseline-1",
            overall_score=0.85,
        ),
        candidate_snapshot=experiment_snapshot(
            experiment_id="candidate-1",
            overall_score=0.80,
        ),
        regression_threshold=0.03,
        notes="Candidate regressed.",
    )

    assert result.score_delta == pytest.approx(-0.05)
    assert result.regression_detected is True
    assert result.interpretation == "regression_detected"
    assert result.notes == "Candidate regressed."
