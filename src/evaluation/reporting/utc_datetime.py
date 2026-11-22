"""Pure UTC normalization for legacy naive and aware report timestamps."""

from __future__ import annotations

from datetime import UTC, datetime


def as_utc(value: datetime) -> datetime:
    """Treat legacy naive datetimes as UTC; normalize aware values to UTC."""
    if value.tzinfo is None or value.utcoffset() is None:
        return value.replace(tzinfo=UTC)
    return value.astimezone(UTC)
