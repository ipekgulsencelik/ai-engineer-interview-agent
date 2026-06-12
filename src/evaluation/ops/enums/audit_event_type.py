from __future__ import annotations

from enum import StrEnum


class AuditEventType(StrEnum):
    EVALUATION_STARTED = "evaluation_started"
    EVALUATION_COMPLETED = "evaluation_completed"
    EVALUATION_FAILED = "evaluation_failed"
    REGRESSION_DETECTED = "regression_detected"
    QUALITY_GATE_EVALUATED = "quality_gate_evaluated"
    CI_POLICY_EVALUATED = "ci_policy_evaluated"