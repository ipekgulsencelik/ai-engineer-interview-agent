from __future__ import annotations

from src.evaluation.reporting.builders.telemetry_attribute_builder import (
    TelemetryAttributeBuilder,
)
from src.evaluation.reporting.entities.telemetry_metric import (
    TelemetryMetric,
)
from src.evaluation.reporting.ports.opentelemetry_metric_client import (
    OpenTelemetryMetricClient,
)


class TelemetryMetricExportService:
    """
    Exports telemetry metrics through a metric client.
    """

    def __init__(
        self,
        *,
        client: OpenTelemetryMetricClient,
        attribute_builder: (
            TelemetryAttributeBuilder
        ),
    ) -> None:
        self._client = client
        self._attribute_builder = (
            attribute_builder
        )

    def export(
        self,
        *,
        metric: TelemetryMetric,
    ) -> None:
        self._client.emit_metric(
            name=metric.metric_name,
            value=float(
                metric.metric_value,
            ),
            unit=metric.unit,
            attributes=self._attribute_builder.build(
                metric=metric,
            ),
        )