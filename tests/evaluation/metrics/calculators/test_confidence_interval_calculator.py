from __future__ import annotations

import pytest

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.metrics.calculators.confidence_interval_calculator import (
    ConfidenceIntervalCalculator,
)
from src.evaluation.metrics.value_objects.confidence_interval import (
    ConfidenceInterval,
)


def test_confidence_interval_calculator_should_calculate_default_interval() -> None:
    interval = ConfidenceIntervalCalculator().calculate(
        values=(10.0, 12.0, 14.0),
    )

    assert isinstance(interval, ConfidenceInterval)
    assert interval.confidence_level == pytest.approx(0.95)
    assert interval.lower_bound == pytest.approx(9.736786, abs=1e-6)
    assert interval.upper_bound == pytest.approx(14.263214, abs=1e-6)
    assert interval.midpoint == pytest.approx(12.0)
    assert interval.margin_of_error == pytest.approx(2.263214, abs=1e-6)
    assert interval.contains(12.0) is True
    assert interval.contains(8.0) is False


def test_confidence_interval_calculator_should_use_custom_confidence_level_and_z_score() -> (
    None
):
    interval = ConfidenceIntervalCalculator().calculate(
        values=(2.0, 4.0, 6.0, 8.0),
        confidence_level=0.90,
        z_score=1.645,
    )

    assert interval.confidence_level == pytest.approx(0.90)
    assert interval.lower_bound == pytest.approx(2.876314, abs=1e-6)
    assert interval.upper_bound == pytest.approx(7.123686, abs=1e-6)
    assert interval.width == pytest.approx(4.247372, abs=1e-6)


def test_confidence_interval_calculator_should_return_zero_width_interval_for_single_value() -> (
    None
):
    interval = ConfidenceIntervalCalculator().calculate(
        values=(42.0,),
    )

    assert interval.lower_bound == pytest.approx(42.0)
    assert interval.upper_bound == pytest.approx(42.0)
    assert interval.width == pytest.approx(0.0)
    assert interval.contains(42.0) is True


@pytest.mark.parametrize(
    "values",
    [
        (),
        (float("nan"),),
        (float("inf"),),
    ],
)
def test_confidence_interval_calculator_should_raise_for_invalid_values(
    values: tuple[float, ...],
) -> None:
    with pytest.raises(EvaluationValidationError):
        ConfidenceIntervalCalculator().calculate(
            values=values,
        )


@pytest.mark.parametrize(
    ("confidence_level", "z_score"),
    [
        (0.0, 1.96),
        (1.0, 1.96),
        (0.95, 0.0),
        (0.95, -1.0),
    ],
)
def test_confidence_interval_calculator_should_raise_for_invalid_parameters(
    confidence_level: float,
    z_score: float,
) -> None:
    with pytest.raises(EvaluationValidationError):
        ConfidenceIntervalCalculator().calculate(
            values=(1.0, 2.0, 3.0),
            confidence_level=confidence_level,
            z_score=z_score,
        )
