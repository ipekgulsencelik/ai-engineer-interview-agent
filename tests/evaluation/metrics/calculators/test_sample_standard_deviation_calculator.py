from __future__ import annotations

import pytest

from src.evaluation.metrics.calculators.sample_standard_deviation_calculator import (
    SampleStandardDeviationCalculator,
)


def test_sample_standard_deviation_calculator_should_calculate_sample_stdev() -> None:
    result = SampleStandardDeviationCalculator.calculate(
        values=(2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0),
    )

    assert result == pytest.approx(2.138089935)


def test_sample_standard_deviation_calculator_should_return_zero_for_identical_values() -> (
    None
):
    result = SampleStandardDeviationCalculator.calculate(
        values=(3.0, 3.0, 3.0),
    )

    assert result == pytest.approx(0.0)


def test_sample_standard_deviation_calculator_should_raise_for_single_value() -> None:
    with pytest.raises(ZeroDivisionError):
        SampleStandardDeviationCalculator.calculate(
            values=(3.0,),
        )
