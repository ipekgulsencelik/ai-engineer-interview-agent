from __future__ import annotations

from typing import Final


DRIFT_SEVERITY_TYPE_ERROR: Final[
    str
] = (
    "severity must be DriftSeverity."
)

ACKNOWLEDGED_BY_REQUIRED_ERROR: Final[
    str
] = (
    "acknowledged_by is required when alert is acknowledged."
)

ACKNOWLEDGED_AT_REQUIRED_ERROR: Final[
    str
] = (
    "acknowledged_at is required when alert is acknowledged."
)

ACKNOWLEDGED_FIELDS_NOT_ALLOWED_ERROR: Final[
    str
] = (
    "acknowledged_by and acknowledged_at must be None "
    "when alert is not acknowledged."
)

ACKNOWLEDGED_AT_BEFORE_CREATED_AT_ERROR: Final[
    str
] = (
    "acknowledged_at cannot be earlier than created_at."
)

DRIFT_DELTA_MISMATCH_ERROR: Final[
    str
] = (
    "drift_delta must equal current_score - baseline_score."
)

ALERT_TRIGGER_MISMATCH_ERROR: Final[
    str
] = (
    "alert_triggered mismatch."
)

NEGATIVE_DRIFT_THRESHOLD_ERROR: Final[
    str
] = (
    "drift_threshold cannot be negative."
)