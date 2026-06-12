from __future__ import annotations

from typing import Final


EVALUATION_RUN_DURATION_TOLERANCE: Final[
    float
] = 1e-6

EXPERIMENT_SNAPSHOT_TYPE_ERROR: Final[
    str
] = (
    "experiment_snapshot must be "
    "ExperimentResultSnapshot."
)

REGRESSION_RESULT_TYPE_ERROR: Final[
    str
] = (
    "regression_result must be "
    "RegressionDetectionResult."
)

QUALITY_GATE_RESULT_TYPE_ERROR: Final[
    str
] = (
    "quality_gate_result must be "
    "QualityGateResult."
)

CI_POLICY_RESULT_TYPE_ERROR: Final[
    str
] = (
    "ci_policy_result must be "
    "CIBenchmarkPolicyResult."
)

COMPLETED_AT_BEFORE_STARTED_AT_ERROR: Final[
    str
] = (
    "completed_at cannot be earlier "
    "than started_at."
)

DURATION_SECONDS_MISMATCH_ERROR: Final[
    str
] = (
    "duration_seconds mismatch."
)

FAILED_RUN_REQUIRES_ERROR_MESSAGE: Final[
    str
] = (
    "Failed evaluation runs must "
    "contain error_message."
)