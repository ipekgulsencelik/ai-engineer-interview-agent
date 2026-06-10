from __future__ import annotations

import pytest

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.metrics.calculators.cohens_dz_calculator import (
    CohensDzCalculator,
)


def test_cohens_dz_calculator_should_calculate_positive_effect_size() -> None:
    result = CohensDzCalculator.calculate(
        differences=(1.0, 2.0, 3.0),
    )

    assert result == pytest.approx(2.0)


def test_cohens_dz_calculator_should_calculate_negative_effect_size() -> None:
    result = CohensDzCalculator.calculate(
        differences=(-1.0, -2.0, -3.0),
    )

    assert result == pytest.approx(-2.0)


def test_cohens_dz_calculator_should_raise_for_constant_differences() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="Cohen's dz is undefined when differences are constant",
    ):
        CohensDzCalculator.calculate(
            differences=(2.0, 2.0, 2.0),
        )
