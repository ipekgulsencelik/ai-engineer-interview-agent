from __future__ import annotations

import pytest

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.metrics.calculators.paired_t_statistic_calculator import (
    PairedTStatisticCalculator,
)


def test_paired_t_statistic_calculator_should_calculate_positive_statistic() -> None:
    result = PairedTStatisticCalculator.calculate(
        differences=(1.0, 2.0, 3.0),
    )

    assert result == pytest.approx(3.464101615)


def test_paired_t_statistic_calculator_should_calculate_negative_statistic() -> None:
    result = PairedTStatisticCalculator.calculate(
        differences=(-1.0, -2.0, -3.0),
    )

    assert result == pytest.approx(-3.464101615)


def test_paired_t_statistic_calculator_should_raise_for_constant_differences() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="paired t-test is undefined when differences are constant",
    ):
        PairedTStatisticCalculator.calculate(
            differences=(1.0, 1.0, 1.0),
        )
