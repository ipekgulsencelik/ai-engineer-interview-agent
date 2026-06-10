from __future__ import annotations

import pytest

from src.evaluation.metrics.calculators.mae_calculator import (
    MAECalculator,
)


def test_mae_calculator_should_calculate_mae() -> None:
    mae = MAECalculator.calculate(
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

    assert mae == pytest.approx(2 / 3)