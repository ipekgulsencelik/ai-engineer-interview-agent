from __future__ import annotations

from statistics import stdev

import pytest

from src.evaluation.metrics.calculators.bootstrap_standard_deviation_calculator import (
    BootstrapStandardDeviationCalculator,
)


def test_bootstrap_standard_deviation_calculator_should_calculate_sample_standard_deviation() -> (
    None
):
    statistic_values = (
        10.0,
        12.0,
        14.0,
        16.0,
    )

    result = BootstrapStandardDeviationCalculator.calculate(
        statistic_values=statistic_values,
    )

    assert result == pytest.approx(stdev(statistic_values))


def test_bootstrap_standard_deviation_calculator_should_return_zero_for_single_value() -> (
    None
):
    result = BootstrapStandardDeviationCalculator.calculate(
        statistic_values=(12.0,),
    )

    assert result == pytest.approx(0.0)


def test_bootstrap_standard_deviation_calculator_should_handle_negative_and_positive_values() -> (
    None
):
    statistic_values = (
        -2.0,
        0.0,
        2.0,
    )

    result = BootstrapStandardDeviationCalculator.calculate(
        statistic_values=statistic_values,
    )

    assert result == pytest.approx(2.0)
