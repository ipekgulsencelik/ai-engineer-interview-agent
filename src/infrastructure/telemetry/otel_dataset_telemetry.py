"""OpenTelemetry SDK adapter for bounded dataset monitoring metrics/traces.

Construction is dependency-injected: providers are configured by the
application composition root, never through process-global mutation.
"""

from __future__ import annotations

import math
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any

_ACTIVITY = frozenset({"monitor", "dispatch"})
_OUTCOME = frozenset({
    "healthy", "warning", "critical", "error",
    "delivered", "retry", "dead_letter",
})


class OpenTelemetryDatasetTelemetry:
    """Only low-cardinality activity/outcome labels enter exported metrics."""

    def __init__(self, *, meter: Any, tracer: Any) -> None:
        self._counter = meter.create_counter(
            "dataset_operations",
            unit="{operation}",
            description="Dataset monitoring operations by bounded outcome",
        )
        self._latency = meter.create_histogram(
            "dataset_operation_duration",
            unit="s",
            description="Dataset monitoring/dispatch duration in seconds",
        )
        self._tracer = tracer

    @staticmethod
    def _activity(value: str) -> None:
        if value not in _ACTIVITY:
            raise ValueError("activity must be monitor or dispatch")

    @contextmanager
    def span(self, *, activity: str) -> Iterator[None]:
        self._activity(activity)
        # record_exception=False prevents exceptions containing sample
        # content or sensitive URLs from being exported as span attributes.
        with self._tracer.start_as_current_span(
            f"dataset.{activity}",
            attributes={"activity": activity},
            record_exception=False,
            set_status_on_exception=False,
        ):
            yield

    def count(self, *, activity: str, outcome: str, amount: int = 1) -> None:
        self._activity(activity)
        if outcome not in _OUTCOME:
            raise ValueError("telemetry outcome is not allowed")
        if type(amount) is not int or amount < 0:
            raise ValueError("telemetry amount must be nonnegative integer")
        if amount:
            self._counter.add(
                amount, {"activity": activity, "outcome": outcome}
            )

    def duration(self, *, activity: str, seconds: float) -> None:
        self._activity(activity)
        if (
            type(seconds) not in (float, int)
            or not math.isfinite(seconds)
            or seconds < 0
        ):
            raise ValueError("telemetry duration must be finite nonnegative")
        self._latency.record(float(seconds), {"activity": activity})
