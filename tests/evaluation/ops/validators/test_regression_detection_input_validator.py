from __future__ import annotations

import pytest

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.ops.validators.regression_detection_input_validator import (
    RegressionDetectionInputValidator,
)
from tests.evaluation.ops.factories import experiment_snapshot


def test_regression_detection_input_validator_should_accept_matching_snapshots() -> None:
    RegressionDetectionInputValidator.validate(
        baseline_snapshot=experiment_snapshot(experiment_id="baseline-1"),
        candidate_snapshot=experiment_snapshot(experiment_id="candidate-1"),
        regression_threshold=0.03,
    )


def test_regression_detection_input_validator_should_raise_for_same_experiment() -> None:
    snapshot = experiment_snapshot(experiment_id="same")

    with pytest.raises(EvaluationValidationError, match="must be different"):
        RegressionDetectionInputValidator.validate(
            baseline_snapshot=snapshot,
            candidate_snapshot=snapshot,
            regression_threshold=0.03,
        )


def test_regression_detection_input_validator_should_raise_for_negative_threshold() -> None:
    with pytest.raises(EvaluationValidationError, match="cannot be negative"):
        RegressionDetectionInputValidator.validate(
            baseline_snapshot=experiment_snapshot(experiment_id="baseline-1"),
            candidate_snapshot=experiment_snapshot(experiment_id="candidate-1"),
            regression_threshold=-0.01,
        )
