"""Pure disaster-recovery evidence evaluation.

This is an evidence-gate, NOT a live RPO/RTO measurement service. Callers
must supply independently verified UTC observations from their drill.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any, Mapping


def parse_timestamp(value: object, field: str) -> datetime:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty RFC3339 timestamp")
    try:
        result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{field} must be an RFC3339 timestamp") from exc
    if result.tzinfo is None or result.utcoffset() is None:
        raise ValueError(f"{field} must contain a UTC offset")
    return result.astimezone(UTC)


def _number(value: object, field: str) -> float:
    if type(value) not in (int, float):
        raise ValueError(f"{field} must be a finite number")
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f"{field} must be a finite number")
    if number < 0:
        raise ValueError(f"{field} cannot be negative")
    return number


@dataclass(frozen=True, slots=True)
class ReadinessPolicy:
    """Thresholds are explicitly selected by operations, not SLA promises."""

    max_backup_age_seconds: float = 93600.0
    max_wal_evidence_age_seconds: float = 900.0
    max_rto_seconds: float = 900.0
    max_rpo_seconds: float = 300.0

    def __post_init__(self) -> None:
        for name in (
            "max_backup_age_seconds",
            "max_wal_evidence_age_seconds",
            "max_rto_seconds",
            "max_rpo_seconds",
        ):
            value = _number(getattr(self, name), name)
            if value <= 0:
                raise ValueError(f"{name} must be positive")


@dataclass(frozen=True, slots=True)
class ReadinessCheck:
    name: str
    passed: bool
    detail: str


@dataclass(frozen=True, slots=True)
class ReadinessReport:
    passed: bool
    checks: tuple[ReadinessCheck, ...]
    observed_metrics_seconds: tuple[tuple[str, float], ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "ready": self.passed,
            "checks": [
                {"check": check.name, "passed": check.passed, "detail": check.detail}
                for check in self.checks
            ],
            "observed_metrics_seconds": dict(self.observed_metrics_seconds),
            "assurance": "operator-supplied evidence only; not an availability SLA",
        }


class ReadinessEvaluator:
    """Deterministic fail-closed evaluation; no Kubernetes or cloud I/O."""

    def __init__(self, *, policy: ReadinessPolicy | None = None) -> None:
        self._policy = policy if policy is not None else ReadinessPolicy()

    def evaluate(self, evidence: Mapping[str, object]) -> ReadinessReport:
        if not isinstance(evidence, Mapping):
            raise ValueError("evidence must be an object")
        now = parse_timestamp(evidence.get("observed_at"), "observed_at")
        checks: list[ReadinessCheck] = []
        metrics: list[tuple[str, float]] = []

        def record(name: str, passed: bool, detail: str) -> None:
            checks.append(ReadinessCheck(name, passed, detail))

        desired = evidence.get("instances_desired")
        ready = evidence.get("instances_ready")
        primary = evidence.get("primary_known")
        healthy = (
            type(desired) is int and type(ready) is int
            and desired == 3 and ready == 3 and primary is True
        )
        record(
            "three_healthy_instances", healthy,
            "requires three ready instances and a primary",
        )

        for field, limit, label in (
            (
                "last_successful_backup_at",
                self._policy.max_backup_age_seconds,
                "backup_age",
            ),
            (
                "last_archived_wal_at",
                self._policy.max_wal_evidence_age_seconds,
                "wal_evidence_age",
            ),
        ):
            raw = evidence.get(field)
            if raw is None:
                record(label, False, "evidence missing")
                continue
            ts = parse_timestamp(raw, field)
            age = (now - ts).total_seconds()
            if age < 0:
                raise ValueError(f"{field} cannot be in the future")
            metrics.append((label, age))
            record(
                label, age <= limit,
                "within threshold" if age <= limit else "older than threshold",
            )

        drill = evidence.get("restore_drill")
        if not isinstance(drill, Mapping):
            record("restore_drill", False, "independent restore evidence missing")
        else:
            verified = drill.get("independently_verified") is True
            record(
                "restore_drill",
                verified,
                "independently verified" if verified else "verification missing",
            )
            required = (
                "incident_declared_at",
                "service_writable_at",
                "latest_committed_at",
                "latest_recovered_commit_at",
            )
            if any(drill.get(name) is None for name in required):
                record("rto", False, "timed recovery evidence missing")
                record("rpo", False, "transaction recovery evidence missing")
            else:
                times = {
                    name: parse_timestamp(drill.get(name), name)
                    for name in required
                }
                rto = (
                    times["service_writable_at"] - times["incident_declared_at"]
                ).total_seconds()
                rpo = (
                    times["latest_committed_at"] - times["latest_recovered_commit_at"]
                ).total_seconds()
                if rto < 0 or rpo < 0:
                    raise ValueError("recovery evidence timestamps are inconsistent")
                if any(ts > now for ts in times.values()):
                    raise ValueError("recovery timestamps cannot be after observation")
                metrics.extend((("rto", rto), ("rpo", rpo)))
                rto_ok = verified and rto <= self._policy.max_rto_seconds
                record(
                    "rto", rto_ok,
                    "within threshold" if rto_ok else "not verified or too slow",
                )
                rpo_ok = verified and rpo <= self._policy.max_rpo_seconds
                record(
                    "rpo", rpo_ok,
                    "within threshold" if rpo_ok else "recovery loss exceeds threshold",
                )

        return ReadinessReport(
            passed=all(check.passed for check in checks),
            checks=tuple(checks),
            observed_metrics_seconds=tuple(metrics),
        )
