"""Fail-closed DR evidence evaluation tests."""

from __future__ import annotations

from copy import deepcopy

import pytest

from src.application.operations.dr_readiness import (
    ReadinessEvaluator,
    ReadinessPolicy,
    parse_timestamp,
)


def evidence() -> dict:
    return {
        "observed_at": "2026-11-22T12:00:00Z",
        "instances_desired": 3,
        "instances_ready": 3,
        "primary_known": True,
        "last_successful_backup_at": "2026-11-22T02:00:00Z",
        "last_archived_wal_at": "2026-11-22T11:55:00Z",
        "restore_drill": {
            "independently_verified": True,
            "incident_declared_at": "2026-11-22T11:20:00Z",
            "service_writable_at": "2026-11-22T11:25:00Z",
            "latest_committed_at": "2026-11-22T11:19:00Z",
            "latest_recovered_commit_at": "2026-11-22T11:18:00Z",
        },
    }


def test_success_and_explicit_elapsed_seconds() -> None:
    report = ReadinessEvaluator().evaluate(evidence())
    assert report.passed
    assert dict(report.observed_metrics_seconds) == {
        "backup_age": 36000,
        "wal_evidence_age": 300,
        "rto": 300,
        "rpo": 60,
    }
    assert "SLA" in report.to_dict()["assurance"]


@pytest.mark.parametrize(
    "key", ["last_successful_backup_at", "last_archived_wal_at", "restore_drill"]
)
def test_missing_evidence_fails_closed(key: str) -> None:
    item = evidence()
    item.pop(key)
    assert not ReadinessEvaluator().evaluate(item).passed


def test_unverified_drill_cannot_pass() -> None:
    item = evidence()
    item["restore_drill"]["independently_verified"] = False
    assert not ReadinessEvaluator().evaluate(item).passed


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("instances_ready", 2),
        ("instances_ready", True),
        ("primary_known", "true"),
        ("last_successful_backup_at", "2026-11-20T00:00:00Z"),
        ("last_archived_wal_at", "2026-11-22T11:00:00Z"),
    ],
)
def test_unhealthy_evidence_fails(field: str, value: object) -> None:
    item = evidence()
    item[field] = value
    assert not ReadinessEvaluator().evaluate(item).passed


def test_breached_rto_or_rpo_threshold() -> None:
    item = evidence()
    item["restore_drill"]["service_writable_at"] = "2026-11-22T11:49:00Z"
    item["restore_drill"]["latest_recovered_commit_at"] = (
        "2026-11-22T11:00:00Z"
    )
    report = ReadinessEvaluator().evaluate(item)
    checks = {c.name: c.passed for c in report.checks}
    assert checks["backup_age"] and checks["wal_evidence_age"]
    assert not checks["rto"] and not checks["rpo"]


@pytest.mark.parametrize("threshold", [0, -1, True, float("nan"), float("inf")])
def test_policy_rejects_invalid_bounds(threshold: float) -> None:
    with pytest.raises(ValueError):
        ReadinessPolicy(max_rpo_seconds=threshold)


@pytest.mark.parametrize(
    "timestamp", ["2026-11-22T12:00:00", "", "nope", True, None]
)
def test_invalid_timestamp_rejected(timestamp: object) -> None:
    with pytest.raises(ValueError):
        parse_timestamp(timestamp, "field")


def test_invalid_order_or_future_evidence_rejected() -> None:
    item = evidence()
    item["restore_drill"]["latest_recovered_commit_at"] = (
        "2026-11-22T11:19:10Z"
    )
    with pytest.raises(ValueError, match="inconsistent"):
        ReadinessEvaluator().evaluate(item)
    item = evidence()
    item["last_successful_backup_at"] = "2026-11-22T13:00:00Z"
    with pytest.raises(ValueError, match="future"):
        ReadinessEvaluator().evaluate(item)


def test_no_untrusted_metadata_in_report() -> None:
    item = deepcopy(evidence())
    item["connection_string"] = "SECRET-CONNECTION"
    item["restore_drill"]["ticket"] = "SECRET-TICKET"
    result = ReadinessEvaluator().evaluate(item)
    assert "SECRET-" not in str(result.to_dict())


def test_custom_thresholds_do_not_modify_defaults() -> None:
    assert not ReadinessEvaluator(
        policy=ReadinessPolicy(max_rpo_seconds=30)
    ).evaluate(evidence()).passed
    assert ReadinessEvaluator().evaluate(evidence()).passed
