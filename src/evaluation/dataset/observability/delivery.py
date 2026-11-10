"""Leased alert-delivery application contracts, independent of SQL and transport."""

from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Protocol

from src.evaluation.dataset.observability.models import MonitoringAlert
from src.evaluation.dataset.observability.ports import AlertSender
from src.evaluation.dataset.observability.telemetry import (
    DatasetTelemetryPort,
    SafeDatasetTelemetry,
)


class AlertLeaseError(RuntimeError):
    """Lease ownership, expiry, or delivery-state preconditions were violated."""


@dataclass(frozen=True, slots=True, kw_only=True)
class AlertLease:
    """A short-lived, fenced claim to deliver one durable alert."""

    alert: MonitoringAlert
    token: str
    worker_id: str
    attempt: int
    expires_at: datetime

    def __post_init__(self) -> None:
        if not isinstance(self.alert, MonitoringAlert):
            raise ValueError("alert must be MonitoringAlert")
        if not isinstance(self.token, str) or not self.token.strip():
            raise ValueError("lease token must not be empty")
        if not isinstance(self.worker_id, str) or not self.worker_id.strip():
            raise ValueError("worker_id must not be empty")
        if type(self.attempt) is not int or self.attempt < 1:
            raise ValueError("attempt must be a positive integer")
        if (
            not isinstance(self.expires_at, datetime)
            or self.expires_at.tzinfo is None
            or self.expires_at.utcoffset() is None
        ):
            raise ValueError("expires_at must be timezone-aware")


@dataclass(frozen=True, slots=True, kw_only=True)
class AlertRetryPolicy:
    """Bounded exponential backoff, with explicit terminal attempt limit."""

    max_attempts: int = 5
    initial_delay_seconds: int = 10
    max_delay_seconds: int = 3600

    def __post_init__(self) -> None:
        if type(self.max_attempts) is not int or not 1 <= self.max_attempts <= 100:
            raise ValueError("max_attempts must be in [1, 100]")
        if (
            type(self.initial_delay_seconds) is not int
            or self.initial_delay_seconds < 1
        ):
            raise ValueError("initial_delay_seconds must be positive")
        if (
            type(self.max_delay_seconds) is not int
            or self.max_delay_seconds < self.initial_delay_seconds
        ):
            raise ValueError(
                "max_delay_seconds must be >= initial_delay_seconds"
            )

    def delay_for_attempt(self, attempt: int) -> int:
        if type(attempt) is not int or attempt < 1:
            raise ValueError("attempt must be a positive integer")
        # Bound exponent before evaluation to avoid unbounded integers.
        return min(
            self.max_delay_seconds,
            self.initial_delay_seconds * (2 ** min(attempt - 1, 30)),
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class AlertFailureOutcome:
    alert_id: str
    attempt: int
    dead_lettered: bool


@dataclass(frozen=True, slots=True, kw_only=True)
class AlertDispatchSummary:
    claimed: int
    delivered: int
    retry_scheduled: int
    dead_lettered: int


class DeliveryClock(Protocol):
    def now(self) -> datetime: ...


class UTCDeliveryClock:
    def now(self) -> datetime:
        return datetime.now(UTC)


class LeasedAlertOutbox(Protocol):
    """Atomic claim, token-fenced acknowledgment, and failure transition."""

    def claim(
        self, *, worker_id: str, limit: int, lease_seconds: int
    ) -> tuple[AlertLease, ...]: ...

    def acknowledge(self, *, lease: AlertLease) -> bool: ...

    def fail(
        self, *, lease: AlertLease, reason_code: str
    ) -> AlertFailureOutcome: ...

    def dead_letters(self, *, limit: int = 100) -> tuple[MonitoringAlert, ...]: ...

    def requeue(self, *, alert_id: str) -> bool: ...


class LeasedDatasetAlertDispatcher:
    """Deliver using fenced claims; transport stays outside the DB transaction.

    Not exactly-once: an expired lease can lead to an external re-send. Senders
    must deduplicate with stable alert.alert_id. Failed acknowledgments are
    propagated, never treated as delivered.
    """

    def __init__(
        self,
        *,
        outbox: LeasedAlertOutbox,
        sender: AlertSender,
        worker_id: str,
        lease_seconds: int = 60,
        telemetry: DatasetTelemetryPort | None = None,
        monotonic_clock: Callable[[], float] | None = None,
    ) -> None:
        if not isinstance(worker_id, str) or not worker_id.strip():
            raise ValueError("worker_id must not be empty")
        if type(lease_seconds) is not int or not 1 <= lease_seconds <= 86400:
            raise ValueError("lease_seconds must be in [1, 86400]")
        self._outbox = outbox
        self._sender = sender
        self._worker_id = worker_id
        self._lease_seconds = lease_seconds
        self._telemetry = SafeDatasetTelemetry(telemetry)
        self._clock = monotonic_clock or time.monotonic

    def dispatch_once(self, *, limit: int = 100) -> AlertDispatchSummary:
        if type(limit) is not int or not 1 <= limit <= 1000:
            raise ValueError("limit must be in [1, 1000]")
        started = self._clock()
        with self._telemetry.span(activity="dispatch"):
            try:
                leases = self._outbox.claim(
                    worker_id=self._worker_id,
                    limit=limit,
                    lease_seconds=self._lease_seconds,
                )
                delivered = retried = dead = 0
                for lease in leases:
                    try:
                        self._sender.send(alert=lease.alert)
                    except Exception:
                        # Never persist raw exception messages (may contain PII).
                        outcome = self._outbox.fail(
                            lease=lease, reason_code="SENDER_FAILURE"
                        )
                        if outcome.dead_lettered:
                            dead += 1
                            label = "dead_letter"
                        else:
                            retried += 1
                            label = "retry"
                        self._telemetry.count(
                            activity="dispatch", outcome=label
                        )
                        continue
                    if not self._outbox.acknowledge(lease=lease):
                        raise AlertLeaseError("delivery acknowledgment rejected")
                    delivered += 1
                    self._telemetry.count(
                        activity="dispatch", outcome="delivered"
                    )
                return AlertDispatchSummary(
                    claimed=len(leases),
                    delivered=delivered,
                    retry_scheduled=retried,
                    dead_lettered=dead,
                )
            except Exception:
                self._telemetry.count(activity="dispatch", outcome="error")
                raise
            finally:
                self._telemetry.duration(
                    activity="dispatch",
                    seconds=max(0.0, self._clock() - started),
                )

