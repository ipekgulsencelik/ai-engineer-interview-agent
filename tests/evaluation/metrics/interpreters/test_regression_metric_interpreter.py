from __future__ import annotations

from src.evaluation.metrics.interpreters.regression_metric_interpreter import (
    RegressionMetricInterpreter,
)


def test_regression_metric_interpreter_should_return_excellent() -> None:
    assert (
        RegressionMetricInterpreter.interpret(
            r2_score=0.95,
        )
        == "excellent"
    )


def test_regression_metric_interpreter_should_return_good() -> None:
    assert (
        RegressionMetricInterpreter.interpret(
            r2_score=0.80,
        )
        == "good"
    )


def test_regression_metric_interpreter_should_return_moderate() -> None:
    assert (
        RegressionMetricInterpreter.interpret(
            r2_score=0.60,
        )
        == "moderate"
    )


def test_regression_metric_interpreter_should_return_poor() -> None:
    assert (
        RegressionMetricInterpreter.interpret(
            r2_score=0.20,
        )
        == "poor"
    )