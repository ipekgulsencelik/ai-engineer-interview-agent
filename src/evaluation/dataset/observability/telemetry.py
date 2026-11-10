"""Narrow telemetry ports and a best-effort privacy-preserving boundary.

Never pass dataset IDs, alert IDs, raw records, exception messages, or
unbounded tag values to telemetry. Monitoring is not a transaction participant.
"""

from __future__ import annotations

import logging
from collections.abc import Iterator
from contextlib import AbstractContextManager, contextmanager
from typing import Protocol


class DatasetTelemetryPort(Protocol):
    """Bounded monitoring signals, independent of any metrics SDK."""

    def span(self, *, activity: str) -> AbstractContextManager[None]: ...

    def count(self, *, activity: str, outcome: str, amount: int = 1) -> None: ...

    def duration(self, *, activity: str, seconds: float) -> None: ...


class NoopDatasetTelemetry:
    @contextmanager
    def span(self, *, activity: str) -> Iterator[None]:
        yield

    def count(self, *, activity: str, outcome: str, amount: int = 1) -> None:
        return

    def duration(self, *, activity: str, seconds: float) -> None:
        return


class SafeDatasetTelemetry:
    """Protect committed business operations from telemetry backend outages."""

    def __init__(self, backend: DatasetTelemetryPort | None = None) -> None:
        self._backend = backend if backend is not None else NoopDatasetTelemetry()
        self._logger = logging.getLogger(__name__)

    def _report_failure(self) -> None:
        # Never log exception text: providers may include URLs or user data.
        self._logger.warning("dataset telemetry exporter unavailable")

    @contextmanager
    def span(self, *, activity: str) -> Iterator[None]:
        context: AbstractContextManager[None] | None = None
        try:
            context = self._backend.span(activity=activity)
            context.__enter__()
        except Exception:
            context = None
            self._report_failure()
        try:
            yield
        finally:
            if context is not None:
                try:
                    context.__exit__(None, None, None)
                except Exception:
                    self._report_failure()

    def count(self, *, activity: str, outcome: str, amount: int = 1) -> None:
        try:
            self._backend.count(
                activity=activity, outcome=outcome, amount=amount
            )
        except Exception:
            self._report_failure()

    def duration(self, *, activity: str, seconds: float) -> None:
        try:
            self._backend.duration(activity=activity, seconds=seconds)
        except Exception:
            self._report_failure()
