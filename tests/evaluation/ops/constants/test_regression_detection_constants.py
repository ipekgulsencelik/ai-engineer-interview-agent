from __future__ import annotations

from src.evaluation.ops.constants import regression_detection


def test_regression_detection_constants_should_define_expected_thresholds() -> None:
    assert regression_detection.DEFAULT_REGRESSION_THRESHOLD == 0.03
    assert regression_detection.DEFAULT_REGRESSION_THRESHOLD > 0


def test_regression_detection_constants_should_define_distinct_interpretations() -> None:
    interpretations = {
        regression_detection.REGRESSION_DETECTED_INTERPRETATION,
        regression_detection.NO_REGRESSION_INTERPRETATION,
        regression_detection.IMPROVEMENT_DETECTED_INTERPRETATION,
    }

    assert interpretations == {
        "regression_detected",
        "no_regression",
        "improvement_detected",
    }
