from __future__ import annotations

import pytest

from src.evaluation.metrics.calculators.mse_calculator import (
    MSECalculator,
)


def test_mse_calculator_should_calculate_mse() -> None:
    mse = MSECalculator.calculate(
        actual_values=(
            3.0,
            5.0,
            7.0,
        ),
        predicted_values=(
            2.0,
            5.0,
            8.0,
        ),
    )

    assert mse == pytest.approx(2 / 3)