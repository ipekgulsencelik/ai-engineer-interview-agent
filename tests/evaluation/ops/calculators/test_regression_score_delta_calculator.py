from __future__ import annotations

import pytest

from src.evaluation.ops.calculators.regression_score_delta_calculator import (
    RegressionScoreDeltaCalculator,
)


@pytest.mark.parametrize(
    ("baseline_score", "candidate_score", "expected_delta"),
    [
        (0.80, 0.75, -0.05),
        (0.80, 0.80, 0.0),
        (0.80, 0.90, 0.10),
    ],
)
def test_regression_score_delta_calculator_should_subtract_baseline(
    baseline_score: float,
    candidate_score: float,
    expected_delta: float,
) -> None:
    assert RegressionScoreDeltaCalculator.calculate(
        baseline_score=baseline_score,
        candidate_score=candidate_score,
    ) == pytest.approx(expected_delta)
