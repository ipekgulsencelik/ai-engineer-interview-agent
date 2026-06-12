from __future__ import annotations

from typing import Final


AUDIT_TRAIL_EVENTS_TYPE_ERROR: Final[str] = (
    "events must be tuple."
)

AUDIT_TRAIL_EVENT_TYPE_ERROR: Final[str] = (
    "events item must be AuditEvent."
)

AUDIT_TRAIL_EMPTY_EVENTS_ERROR: Final[str] = (
    "events cannot be empty."
)

AUDIT_TRAIL_EVENT_EXPERIMENT_MISMATCH_ERROR: Final[
    str
] = (
    "event experiment_id mismatch."
)

AUDIT_TRAIL_EVENT_BENCHMARK_MISMATCH_ERROR: Final[
    str
] = (
    "event benchmark_id mismatch."
)

AUDIT_TRAIL_EVENT_ORDER_ERROR: Final[str] = (
    "events must be ordered by occurred_at."
)