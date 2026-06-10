from __future__ import annotations

import pytest

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.metrics.calculators.pearson_coefficient_calculator import (
    PearsonCoefficientCalculator,
)


def test_pearson_coefficient_calculator_should_calculate_perfect_positive_correlation() -> (
    None
):
    result = PearsonCoefficientCalculator.calculate(
        x_values=(1.0, 2.0, 3.0),
        y_values=(2.0, 4.0, 6.0),
    )

    assert result == pytest.approx(1.0)


def test_pearson_coefficient_calculator_should_calculate_perfect_negative_correlation() -> (
    None
):
    result = PearsonCoefficientCalculator.calculate(
        x_values=(1.0, 2.0, 3.0),
        y_values=(3.0, 2.0, 1.0),
    )

    assert result == pytest.approx(-1.0)


def test_pearson_coefficient_calculator_should_calculate_partial_correlation() -> None:
    result = PearsonCoefficientCalculator.calculate(
        x_values=(1.0, 2.0, 3.0, 4.0),
        y_values=(1.0, 3.0, 2.0, 5.0),
    )

    assert result == pytest.approx(0.831521841)


@pytest.mark.parametrize(
    ("x_values", "y_values"),
    [
        ((1.0, 1.0, 1.0), (2.0, 3.0, 4.0)),
        ((1.0, 2.0, 3.0), (4.0, 4.0, 4.0)),
    ],
)
def test_pearson_coefficient_calculator_should_raise_for_constant_values(
    x_values: tuple[float, ...],
    y_values: tuple[float, ...],
) -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="Pearson correlation is undefined for constant values",
    ):
        PearsonCoefficientCalculator.calculate(
            x_values=x_values,
            y_values=y_values,
        )


def test_pearson_coefficient_calculator_should_raise_for_mismatched_lengths() -> None:
    with pytest.raises(ValueError):
        PearsonCoefficientCalculator.calculate(
            x_values=(1.0, 2.0),
            y_values=(1.0,),
        )
