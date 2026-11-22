"""Storage port for scheduled reports (dependency inversion boundary).

Adapters may be backed by SQL, files or memory; this module performs no I/O.
"""

from __future__ import annotations

from typing import Protocol

from src.evaluation.reporting.entities.schedule_report import ScheduledReport


class ScheduledReportStore(Protocol):
    """Minimal contract required by the scheduler and state service."""

    def list_enabled(self) -> tuple[ScheduledReport, ...]:
        """Read enabled scheduled jobs without exposing storage details."""
        ...

    def update(self, *, scheduled_report: ScheduledReport) -> None:
        """Persist a new immutable report schedule snapshot."""
        ...
