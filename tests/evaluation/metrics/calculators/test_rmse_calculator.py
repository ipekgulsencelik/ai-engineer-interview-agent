from __future__ import annotations

import pytest

from src.evaluation.metrics.calculators.rmse_calculator import (
    RMSECalculator,
)


def test_rmse_calculator_should_calculate_rmse() -> None:
    rmse = RMSECalculator.calculate(
        mse=4.0,
    )

    assert rmse == pytest.approx(2.0)