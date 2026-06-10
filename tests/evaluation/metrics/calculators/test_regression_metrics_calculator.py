from __future__ import annotations

import pytest

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.metrics.calculators.regression_metrics_calculator import (
    RegressionMetricsCalculator,
)


def test_regression_metrics_calculator_should_calculate_metrics_successfully() -> None:
    result = RegressionMetricsCalculator.calculate(
        metric_name="human_llm_score_regression",
        actual_values=(
            3.0,
            5.0,
            7.0,
            9.0,
        ),
        predicted_values=(
            2.5,
            5.0,
            7.5,
            9.0,
        ),
        notes="Regression metric test.",
    )

    assert result.metric_name == "human_llm_score_regression"
    assert result.mae == pytest.approx(0.25)
    assert result.mse == pytest.approx(0.125)
    assert result.rmse == pytest.approx(0.3535533905)
    assert result.r2_score == pytest.approx(0.975)
    assert result.sample_count == 4
    assert result.is_acceptable is True
    assert result.interpretation == "excellent"
    assert result.notes == "Regression metric test."


def test_regression_metrics_calculator_should_raise_for_mismatched_lengths() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="actual_values and predicted_values must have the same length",
    ):
        RegressionMetricsCalculator.calculate(
            metric_name="regression",
            actual_values=(
                1.0,
                2.0,
            ),
            predicted_values=(
                1.0,
            ),
        )


def test_regression_metrics_calculator_should_raise_for_empty_values() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="regression metrics require at least 1 value",
    ):
        RegressionMetricsCalculator.calculate(
            metric_name="regression",
            actual_values=(),
            predicted_values=(),
        )


@pytest.mark.parametrize(
    "invalid_value",
    [
        "1.0",
        True,
    ],
)
def test_regression_metrics_calculator_should_raise_for_non_numeric_actual_values(
    invalid_value: object,
) -> None:
    with pytest.raises(
        EvaluationValidationError,
        match=r"actual_values\[0\] must be numeric",
    ):
        RegressionMetricsCalculator.calculate(
            metric_name="regression",
            actual_values=(
                invalid_value,  # type: ignore[arg-type]
                2.0,
            ),
            predicted_values=(
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
def test_regression_metrics_calculator_should_raise_for_non_finite_predicted_values(
    invalid_value: float,
) -> None:
    with pytest.raises(
        EvaluationValidationError,
        match=r"predicted_values\[0\] must be finite",
    ):
        RegressionMetricsCalculator.calculate(
            metric_name="regression",
            actual_values=(
                1.0,
                2.0,
            ),
            predicted_values=(
                invalid_value,
                2.0,
            ),
        )


def test_regression_metrics_calculator_should_raise_for_constant_actual_values() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="R2 score is undefined when actual values are constant",
    ):
        RegressionMetricsCalculator.calculate(
            metric_name="regression",
            actual_values=(
                1.0,
                1.0,
                1.0,
            ),
            predicted_values=(
                1.0,
                1.0,
                1.0,
            ),
        )