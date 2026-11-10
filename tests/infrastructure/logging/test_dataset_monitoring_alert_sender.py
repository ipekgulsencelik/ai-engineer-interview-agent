"""Metadata-only structured log delivery for monitoring alert signals."""

from __future__ import annotations

import logging

import pytest

from src.evaluation.dataset.observability import (
    AlertSeverity,
    MonitoringAlert,
)
from src.infrastructure.logging.dataset_monitoring_alert_sender import (
    LoggingMonitoringAlertSender,
)


def test_logging_sender_emits_stable_fields_without_sample_values(
    caplog: pytest.LogCaptureFixture,
) -> None:
    logger = logging.getLogger("dataset.monitoring.test")
    alert = MonitoringAlert(
        alert_id="run-1:DRIFT_WARNING",
        code="DRIFT_WARNING",
        severity=AlertSeverity.WARNING,
        metric="distribution_drift",
        observed=0.2,
        threshold=0.1,
    )
    with caplog.at_level(logging.WARNING, logger=logger.name):
        LoggingMonitoringAlertSender(logger=logger).send(alert=alert)
    assert len(caplog.records) == 1
    record = caplog.records[0]
    assert getattr(record, "dataset_alert_id") == alert.alert_id
    assert getattr(record, "dataset_alert_observed") == 0.2
    assert "private candidate answer" not in caplog.text
