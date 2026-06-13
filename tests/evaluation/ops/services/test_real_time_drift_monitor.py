from __future__ import annotations

from datetime import datetime, timezone

import pytest

from src.evaluation.ops.enums.drift_severity import DriftSeverity
from src.evaluation.ops.services.real_time_drift_monitor import RealTimeDriftMonitor
from tests.evaluation.ops.factories import experiment_snapshot


def test_real_time_drift_monitor_should_emit_negative_drift_alert() -> None:
    created_at = datetime(2026, 1, 1, tzinfo=timezone.utc)

    alert = RealTimeDriftMonitor().evaluate(
        baseline_snapshot=experiment_snapshot(
            experiment_id="baseline-exp",
            overall_score=0.90,
        ),
        current_snapshot=experiment_snapshot(
            experiment_id="current-exp",
            overall_score=0.70,
        ),
        drift_threshold=0.10,
        created_at=created_at,
        notes="nightly drift check",
    )

    assert alert.alert_triggered is True
    assert alert.requires_attention is True
    assert alert.is_acknowledged is False
    assert alert.is_regression_drift is True
    assert alert.is_improvement_drift is False
    assert alert.drift_delta == pytest.approx(-0.20)
    assert alert.drift_magnitude == pytest.approx(0.20)
    assert alert.severity == DriftSeverity.CRITICAL
    assert alert.interpretation == "negative_drift_detected"
    assert alert.created_at == created_at
    assert alert.notes == "nightly drift check"


def test_real_time_drift_monitor_should_keep_small_drift_within_threshold() -> None:
    alert = RealTimeDriftMonitor().evaluate(
        baseline_snapshot=experiment_snapshot(overall_score=0.80),
        current_snapshot=experiment_snapshot(overall_score=0.85),
        drift_threshold=0.10,
    )

    assert alert.alert_triggered is False
    assert alert.requires_attention is False
    assert alert.severity == DriftSeverity.INFO
    assert alert.interpretation == "drift_within_threshold"
