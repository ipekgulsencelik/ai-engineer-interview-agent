from __future__ import annotations

from src.evaluation.reporting.entities.telemetry_metric import (
    TelemetryMetric,
)
from src.evaluation.reporting.services.telemetry_metric_export_service import (
    TelemetryMetricExportService,
)


class OpenTelemetryExporter:
    """
    Facade exporter for telemetry metrics.
    """

    def __init__(
        self,
        *,
        export_service: (
            TelemetryMetricExportService
        ),
    ) -> None:
        self._export_service = (
            export_service
        )

    def export(
        self,
        *,
        metric: TelemetryMetric,
    ) -> None:
        self._export_service.export(
            metric=metric,
        )

    def export_many(
        self,
        *,
        metrics: tuple[
            TelemetryMetric,
            ...,
        ],
    ) -> None:
        for metric in metrics:
            self.export(
                metric=metric,
            )