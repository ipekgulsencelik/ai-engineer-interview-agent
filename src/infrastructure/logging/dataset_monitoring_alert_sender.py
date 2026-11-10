"""Structured log sender for durable dataset monitoring alerts."""

from __future__ import annotations

import logging

from src.evaluation.dataset.observability.models import MonitoringAlert


class LoggingMonitoringAlertSender:
    """Emit redacted alert metadata; a log entry is not external notification."""

    def __init__(self, logger: logging.Logger | None = None) -> None:
        self._logger = (
            logger if logger is not None
            else logging.getLogger("dataset.observability.alerts")
        )

    def send(self, *, alert: MonitoringAlert) -> None:
        self._logger.warning(
            "dataset monitoring alert %s (%s)",
            alert.code,
            alert.severity.value,
            extra={
                "dataset_alert_id": alert.alert_id,
                "dataset_alert_code": alert.code,
                "dataset_alert_severity": alert.severity.value,
                "dataset_alert_metric": alert.metric,
                "dataset_alert_observed": alert.observed,
                "dataset_alert_threshold": alert.threshold,
            },
        )
