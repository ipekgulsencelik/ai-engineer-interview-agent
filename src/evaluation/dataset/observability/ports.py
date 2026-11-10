"""Minimal read/write and delivery boundaries for monitoring."""

from __future__ import annotations

from typing import Protocol

from src.evaluation.dataset.observability.models import (
    MonitoringAlert,
    MonitoringSnapshot,
)


class MonitoringWriter(Protocol):
    def save(self, *, snapshot: MonitoringSnapshot) -> bool: ...


class MonitoringReader(Protocol):
    def get(self, *, monitor_run_id: str) -> MonitoringSnapshot | None: ...

    def list_snapshots(
        self, *, dataset_id: str, limit: int = 100
    ) -> tuple[MonitoringSnapshot, ...]: ...


class AlertOutbox(Protocol):
    def pending(
        self, *, limit: int = 100
    ) -> tuple[MonitoringAlert, ...]: ...

    def mark_delivered(self, *, alert_id: str) -> bool: ...


class AlertSender(Protocol):
    def send(self, *, alert: MonitoringAlert) -> None: ...
