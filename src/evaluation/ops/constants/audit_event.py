from __future__ import annotations

from typing import Final


AUDIT_EVENT_TYPE_ERROR: Final[str] = (
    "event_type must be AuditEventType."
)

AUDIT_ACTION_TYPE_ERROR: Final[str] = (
    "action must be AuditAction."
)

AUDIT_AGGREGATE_TYPE_ERROR: Final[str] = (
    "aggregate_type must be AuditAggregateType."
)

AUDIT_TRIGGER_TYPE_ERROR: Final[str] = (
    "triggered_by must be AuditTrigger."
)

AUDIT_METADATA_TYPE_ERROR: Final[str] = (
    "metadata must be a mapping."
)

AUDIT_METADATA_KEY_TYPE_ERROR: Final[str] = (
    "metadata keys must be strings."
)

AUDIT_METADATA_VALUE_TYPE_ERROR: Final[str] = (
    "metadata values must be str, int, float, or bool."
)