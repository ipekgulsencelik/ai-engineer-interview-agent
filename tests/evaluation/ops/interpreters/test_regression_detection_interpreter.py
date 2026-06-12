from __future__ import annotations

from src.evaluation.ops.constants.regression_detection import (
    IMPROVEMENT_DETECTED_INTERPRETATION,
    NO_REGRESSION_INTERPRETATION,
    REGRESSION_DETECTED_INTERPRETATION,
)
from src.evaluation.ops.interpreters.regression_detection_interpreter import (
    RegressionDetectionInterpreter,
)


def test_regression_detection_interpreter_should_flag_threshold_regression() -> None:
    assert RegressionDetectionInterpreter.interpret(
        score_delta=-0.03,
        regression_threshold=0.03,
    ) == REGRESSION_DETECTED_INTERPRETATION


def test_regression_detection_interpreter_should_flag_improvement() -> None:
    assert RegressionDetectionInterpreter.interpret(
        score_delta=0.01,
        regression_threshold=0.03,
    ) == IMPROVEMENT_DETECTED_INTERPRETATION


def test_regression_detection_interpreter_should_flag_no_regression() -> None:
    assert RegressionDetectionInterpreter.interpret(
        score_delta=-0.02,
        regression_threshold=0.03,
    ) == NO_REGRESSION_INTERPRETATION
