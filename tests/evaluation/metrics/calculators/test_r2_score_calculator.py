from __future__ import annotations

import pytest

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.metrics.calculators.r2_score_calculator import (
    R2ScoreCalculator,
)


def test_r2_score_calculator_should_calculate_r2_score() -> None:
    r2_score = R2ScoreCalculator.calculate(
        actual_values=(
            3.0,
            5.0,
            7.0,
            9.0,
        ),
        predicted_values=(
            2.5,
            5.0,
            7.5,
            9.0,
        ),
    )

    assert r2_score == pytest.approx(0.975)


def test_r2_score_calculator_should_raise_for_constant_actual_values() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="R2 score is undefined when actual values are constant",
    ):
        R2ScoreCalculator.calculate(
            actual_values=(
                1.0,
                1.0,
                1.0,
            ),
            predicted_values=(
                1.0,
                1.0,
                1.0,
            ),
        )