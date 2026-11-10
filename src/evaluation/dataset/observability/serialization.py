"""Stable JSON-safe, content-verifiable monitoring snapshot serialization."""

from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime
from typing import Any

from src.evaluation.dataset.observability.models import (
    AlertSeverity,
    MonitoringAlert,
    MonitoringPolicy,
    MonitoringSnapshot,
    MonitoringStatus,
)


def alert_to_dict(alert: MonitoringAlert) -> dict[str, Any]:
    return {
        "alert_id": alert.alert_id,
        "code": alert.code,
        "severity": alert.severity.value,
        "metric": alert.metric,
        "observed": alert.observed,
        "threshold": alert.threshold,
    }


def alert_from_dict(data: dict[str, Any]) -> MonitoringAlert:
    return MonitoringAlert(
        alert_id=data["alert_id"],
        code=data["code"],
        severity=AlertSeverity(data["severity"]),
        metric=data["metric"],
        observed=data["observed"],
        threshold=data["threshold"],
    )


class MonitoringSnapshotSerializer:
    @staticmethod
    def serialize(snapshot: MonitoringSnapshot) -> dict[str, Any]:
        return {
            "monitor_run_id": snapshot.monitor_run_id,
            "dataset_id": snapshot.dataset_id,
            "dataset_version": snapshot.dataset_version,
            "baseline_dataset_id": snapshot.baseline_dataset_id,
            "baseline_dataset_version": snapshot.baseline_dataset_version,
            "baseline_quality_run_id": snapshot.baseline_quality_run_id,
            "comparison_quality_run_id": snapshot.comparison_quality_run_id,
            "recorded_at": snapshot.recorded_at.isoformat(),
            "record_count": snapshot.record_count,
            "baseline_pass_rate": snapshot.baseline_pass_rate,
            "comparison_pass_rate": snapshot.comparison_pass_rate,
            "pass_rate_drop": snapshot.pass_rate_drop,
            "drift_score": snapshot.drift_score,
            "status": snapshot.status.value,
            "policy": asdict(snapshot.policy),
            "alerts": [alert_to_dict(alert) for alert in snapshot.alerts],
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> MonitoringSnapshot:
        return MonitoringSnapshot(
            monitor_run_id=data["monitor_run_id"],
            dataset_id=data["dataset_id"],
            dataset_version=data["dataset_version"],
            baseline_dataset_id=data["baseline_dataset_id"],
            baseline_dataset_version=data["baseline_dataset_version"],
            baseline_quality_run_id=data["baseline_quality_run_id"],
            comparison_quality_run_id=data["comparison_quality_run_id"],
            recorded_at=datetime.fromisoformat(data["recorded_at"]),
            record_count=data["record_count"],
            baseline_pass_rate=data["baseline_pass_rate"],
            comparison_pass_rate=data["comparison_pass_rate"],
            pass_rate_drop=data["pass_rate_drop"],
            drift_score=data["drift_score"],
            status=MonitoringStatus(data["status"]),
            policy=MonitoringPolicy(**data["policy"]),
            alerts=tuple(alert_from_dict(alert) for alert in data["alerts"]),
        )


def canonical_json(data: dict[str, Any]) -> str:
    return json.dumps(
        data, sort_keys=True, separators=(",", ":"),
        ensure_ascii=False, allow_nan=False,
    )
