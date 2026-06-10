from __future__ import annotations

import pytest

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.metrics.value_objects.regression_metric_result import (
    RegressionMetricResult,
)


def test_regression_metric_result_should_create_successfully() -> None:
    result = RegressionMetricResult(
        metric_name="score_regression",
        mae=0.25,
        mse=0.125,
        rmse=0.3535,
        r2_score=0.975,
        sample_count=4,
        is_acceptable=True,
        interpretation="excellent",
        notes="Valid result.",
    )

    assert result.metric_name == "score_regression"
    assert result.mae == 0.25
    assert result.mse == 0.125
    assert result.rmse == 0.3535
    assert result.r2_score == 0.975
    assert result.sample_count == 4
    assert result.is_acceptable is True
    assert result.interpretation == "excellent"
    assert result.notes == "Valid result."


def test_regression_metric_result_should_be_immutable() -> None:
    result = RegressionMetricResult(
        metric_name="score_regression",
        mae=0.25,
        mse=0.125,
        rmse=0.3535,
        r2_score=0.975,
        sample_count=4,
        is_acceptable=True,
        interpretation="excellent",
    )

    with pytest.raises(
        AttributeError,
    ):
        result.metric_name = "changed"  # type: ignore[misc]


def test_regression_metric_result_should_raise_for_invalid_r2_score() -> None:
    with pytest.raises(
        EvaluationValidationError,
    ):
        RegressionMetricResult(
            metric_name="score_regression",
            mae=0.25,
            mse=0.125,
            rmse=0.3535,
            r2_score=2.0,
            sample_count=4,
            is_acceptable=True,
            interpretation="excellent",
        )


def test_regression_metric_result_should_raise_for_negative_error_metric() -> None:
    with pytest.raises(
        EvaluationValidationError,
    ):
        RegressionMetricResult(
            metric_name="score_regression",
            mae=-0.25,
            mse=0.125,
            rmse=0.3535,
            r2_score=0.975,
            sample_count=4,
            is_acceptable=True,
            interpretation="excellent",
        )