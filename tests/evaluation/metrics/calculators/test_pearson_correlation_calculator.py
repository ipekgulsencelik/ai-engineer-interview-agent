from __future__ import annotations

import pytest

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.metrics.calculators.pearson_correlation_calculator import (
    PearsonCorrelationCalculator,
)


def test_pearson_correlation_calculator_should_calculate_positive_correlation() -> None:
    result = PearsonCorrelationCalculator.calculate(
        metric_x="human_score",
        metric_y="llm_score",
        x_values=(
            1.0,
            2.0,
            3.0,
            4.0,
        ),
        y_values=(
            2.0,
            4.0,
            6.0,
            8.0,
        ),
        p_value=0.01,
    )

    assert result.metric_x == "human_score"
    assert result.metric_y == "llm_score"
    assert result.correlation_coefficient == pytest.approx(
        1.0,
    )
    assert result.p_value == 0.01
    assert result.sample_count == 4
    assert result.method == "pearson"
    assert result.is_significant is True
    assert result.interpretation == "very_strong"


def test_pearson_correlation_calculator_should_calculate_negative_correlation() -> None:
    result = PearsonCorrelationCalculator.calculate(
        metric_x="human_score",
        metric_y="llm_score",
        x_values=(
            1.0,
            2.0,
            3.0,
        ),
        y_values=(
            3.0,
            2.0,
            1.0,
        ),
        p_value=0.20,
    )

    assert result.correlation_coefficient == pytest.approx(
        -1.0,
    )
    assert result.is_significant is False
    assert result.interpretation == "very_strong"


def test_pearson_correlation_calculator_should_calculate_zero_correlation() -> None:
    result = PearsonCorrelationCalculator.calculate(
        metric_x="x",
        metric_y="y",
        x_values=(
            -1.0,
            0.0,
            1.0,
            0.0,
        ),
        y_values=(
            0.0,
            1.0,
            0.0,
            -1.0,
        ),
        p_value=1.0,
    )

    assert result.correlation_coefficient == pytest.approx(
        0.0,
    )
    assert result.interpretation == "very_weak"


def test_pearson_correlation_calculator_should_raise_for_mismatched_lengths() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="x_values and y_values must have the same length",
    ):
        PearsonCorrelationCalculator.calculate(
            metric_x="human_score",
            metric_y="llm_score",
            x_values=(
                1.0,
                2.0,
            ),
            y_values=(
                1.0,
            ),
        )


def test_pearson_correlation_calculator_should_raise_for_too_few_values() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="correlation requires at least 2 values",
    ):
        PearsonCorrelationCalculator.calculate(
            metric_x="human_score",
            metric_y="llm_score",
            x_values=(
                1.0,
            ),
            y_values=(
                1.0,
            ),
        )


@pytest.mark.parametrize(
    "invalid_value",
    [
        "1.0",
        True,
    ],
)
def test_pearson_correlation_calculator_should_raise_for_non_numeric_values(
    invalid_value: object,
) -> None:
    with pytest.raises(
        EvaluationValidationError,
        match=r"x_values\[0\] must be numeric",
    ):
        PearsonCorrelationCalculator.calculate(
            metric_x="human_score",
            metric_y="llm_score",
            x_values=(
                invalid_value,  # type: ignore[arg-type]
                2.0,
            ),
            y_values=(
                1.0,
                2.0,
            ),
        )


@pytest.mark.parametrize(
    "invalid_value",
    [
        float("nan"),
        float("inf"),
        float("-inf"),
    ],
)
def test_pearson_correlation_calculator_should_raise_for_non_finite_values(
    invalid_value: float,
) -> None:
    with pytest.raises(
        EvaluationValidationError,
        match=r"x_values\[0\] must be finite",
    ):
        PearsonCorrelationCalculator.calculate(
            metric_x="human_score",
            metric_y="llm_score",
            x_values=(
                invalid_value,
                2.0,
            ),
            y_values=(
                1.0,
                2.0,
            ),
        )


def test_pearson_correlation_calculator_should_raise_for_constant_x_values() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="Pearson correlation is undefined for constant values",
    ):
        PearsonCorrelationCalculator.calculate(
            metric_x="human_score",
            metric_y="llm_score",
            x_values=(
                1.0,
                1.0,
                1.0,
            ),
            y_values=(
                1.0,
                2.0,
                3.0,
            ),
        )


def test_pearson_correlation_calculator_should_raise_for_invalid_p_value() -> None:
    with pytest.raises(
        EvaluationValidationError,
    ):
        PearsonCorrelationCalculator.calculate(
            metric_x="human_score",
            metric_y="llm_score",
            x_values=(
                1.0,
                2.0,
                3.0,
            ),
            y_values=(
                1.0,
                2.0,
                3.0,
            ),
            p_value=1.1,
        )