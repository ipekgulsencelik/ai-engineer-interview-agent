"""Application-level monitoring and reliable alert delivery orchestration."""

from __future__ import annotations

import logging
import time
from collections.abc import Callable
from typing import Protocol

from src.evaluation.dataset.observability.errors import AlertDeliveryError
from src.evaluation.dataset.observability.models import MonitoringSnapshot
from src.evaluation.dataset.observability.ports import (
    AlertOutbox,
    AlertSender,
    MonitoringWriter,
)
from src.evaluation.dataset.observability.telemetry import (
    DatasetTelemetryPort,
    SafeDatasetTelemetry,
)
from src.evaluation.dataset.quality.models import QualityReport
from src.evaluation.dataset.value_objects.dataset_distribution_snapshot import (
    DatasetDistributionSnapshot,
)


class MonitorEvaluatorPort(Protocol):
    def evaluate(
        self,
        *,
        baseline_distribution: DatasetDistributionSnapshot,
        comparison_distribution: DatasetDistributionSnapshot,
        baseline_quality: QualityReport,
        comparison_quality: QualityReport,
    ) -> MonitoringSnapshot: ...


class DatasetObservabilityCoordinator:
    """Store snapshot and pending alerts atomically before dispatch."""

    def __init__(
        self,
        *,
        monitor: MonitorEvaluatorPort,
        store: MonitoringWriter,
        telemetry: DatasetTelemetryPort | None = None,
        monotonic_clock: Callable[[], float] | None = None,
    ) -> None:
        self._monitor = monitor
        self._store = store
        self._telemetry = SafeDatasetTelemetry(telemetry)
        self._clock = monotonic_clock or time.monotonic

    def evaluate_and_store(
        self,
        *,
        baseline_distribution: DatasetDistributionSnapshot,
        comparison_distribution: DatasetDistributionSnapshot,
        baseline_quality: QualityReport,
        comparison_quality: QualityReport,
    ) -> MonitoringSnapshot:
        started = self._clock()
        with self._telemetry.span(activity="monitor"):
            try:
                snapshot = self._monitor.evaluate(
                    baseline_distribution=baseline_distribution,
                    comparison_distribution=comparison_distribution,
                    baseline_quality=baseline_quality,
                    comparison_quality=comparison_quality,
                )
                self._store.save(snapshot=snapshot)
            except Exception:
                self._telemetry.count(activity="monitor", outcome="error")
                raise
            else:
                self._telemetry.count(
                    activity="monitor", outcome=snapshot.status.value
                )
                return snapshot
            finally:
                self._telemetry.duration(
                    activity="monitor",
                    seconds=max(0.0, self._clock() - started),
                )


class DatasetAlertDispatcher:
    """At-least-once delivery; caller must schedule and retry as necessary.

    Alert senders should deduplicate using the stable alert_id. Never
    acknowledge a failed delivery. Delivery happens outside SQLite transactions.
    """

    def __init__(self, *, outbox: AlertOutbox, sender: AlertSender) -> None:
        self._outbox = outbox
        self._sender = sender

    def dispatch_pending(self, *, limit: int = 100) -> int:
        alerts = self._outbox.pending(limit=limit)
        delivered = 0
        for alert in alerts:
            try:
                self._sender.send(alert=alert)
            except Exception as exc:
                logging.getLogger(__name__).warning(
                    "dataset alert dispatch failed; alert remains pending",
                    extra={"dataset_alert_id": alert.alert_id},
                )
                raise AlertDeliveryError(
                    "alert delivery failed; retry pending outbox"
                ) from exc
            # A crash between send and ack may duplicate sends on retry.
            self._outbox.mark_delivered(alert_id=alert.alert_id)
            delivered += 1
        return delivered
