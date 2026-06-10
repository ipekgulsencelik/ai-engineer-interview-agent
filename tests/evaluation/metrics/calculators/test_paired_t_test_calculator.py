from __future__ import annotations

import pytest

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.metrics.calculators.paired_t_test_calculator import (
    PairedTTestCalculator,
)
from src.evaluation.metrics.value_objects.significance_test_result import (
    SignificanceTestResult,
)


def test_paired_t_test_calculator_should_return_significant_result() -> None:
    result = PairedTTestCalculator.calculate(
        before_values=(1.0, 2.0, 3.0),
        after_values=(2.0, 4.0, 6.0),
        p_value=0.01,
        notes="paired t-test",
    )

    assert isinstance(result, SignificanceTestResult)
    assert result.test_name == "paired_t_test"
    assert result.statistic == pytest.approx(3.464101615)
    assert result.effect_size == pytest.approx(2.0)
    assert result.p_value == pytest.approx(0.01)
    assert result.alpha == pytest.approx(0.05)
    assert result.is_significant is True
    assert result.rejects_null_hypothesis is True
    assert result.retains_null_hypothesis is False
    assert result.sample_count == 3
    assert result.notes == "paired t-test"


def test_paired_t_test_calculator_should_return_non_significant_result_with_custom_alpha() -> (
    None
):
    result = PairedTTestCalculator.calculate(
        before_values=(1.0, 2.0, 3.0),
        after_values=(2.0, 4.0, 6.0),
        p_value=0.10,
        alpha=0.01,
        interpretation="not significant",
    )

    assert result.is_significant is False
    assert result.rejects_null_hypothesis is False
    assert result.retains_null_hypothesis is True
    assert result.alpha == pytest.approx(0.01)
    assert result.interpretation == "not significant"


@pytest.mark.parametrize(
    ("before_values", "after_values", "p_value", "alpha"),
    [
        ((1.0,), (2.0,), 0.01, 0.05),
        ((1.0, 2.0), (2.0,), 0.01, 0.05),
        ((1.0, 2.0), (2.0, 3.0), -0.01, 0.05),
        ((1.0, 2.0), (2.0, 3.0), 0.01, 0.0),
    ],
)
def test_paired_t_test_calculator_should_raise_for_invalid_input(
    before_values: tuple[float, ...],
    after_values: tuple[float, ...],
    p_value: float,
    alpha: float,
) -> None:
    with pytest.raises(EvaluationValidationError):
        PairedTTestCalculator.calculate(
            before_values=before_values,
            after_values=after_values,
            p_value=p_value,
            alpha=alpha,
        )
