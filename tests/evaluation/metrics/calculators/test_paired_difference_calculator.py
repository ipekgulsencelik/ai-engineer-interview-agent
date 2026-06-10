from __future__ import annotations

import pytest

from src.evaluation.metrics.calculators.paired_difference_calculator import (
    PairedDifferenceCalculator,
)


def test_paired_difference_calculator_should_return_after_minus_before() -> None:
    result = PairedDifferenceCalculator.calculate(
        before_values=(1.0, 2.0, 4.0),
        after_values=(2.0, 5.0, 7.0),
    )

    assert result == (1.0, 3.0, 3.0)


def test_paired_difference_calculator_should_support_negative_differences() -> None:
    result = PairedDifferenceCalculator.calculate(
        before_values=(5.0, 4.0, 3.0),
        after_values=(3.0, 4.5, 1.0),
    )

    assert result == (-2.0, 0.5, -2.0)


def test_paired_difference_calculator_should_raise_for_mismatched_lengths() -> None:
    with pytest.raises(ValueError):
        PairedDifferenceCalculator.calculate(
            before_values=(1.0, 2.0),
            after_values=(2.0,),
        )
