from __future__ import annotations

from typing import Any

from src.evaluation.reporting.entities.telemetry_metric import (
    TelemetryMetric,
)


class TelemetryMetricBIRowMapper:
    """
    Maps telemetry metrics to BI rows.
    """

    def to_row(
        self,
        *,
        metric: TelemetryMetric,
    ) -> dict[
        str,
        Any,
    ]:
        row = {
            "metric_id": metric.metric_id,
            "metric_name": metric.metric_name,
            "metric_value": metric.metric_value,
            "unit": metric.unit,
            "source": metric.source,
            "recorded_at": metric.recorded_at.isoformat(),
            "tenant_id": metric.tenant_id,
            "experiment_id": metric.experiment_id,
            "run_id": metric.run_id,
            "report_id": metric.report_id,
            "artifact_id": metric.artifact_id,
            "worker_id": metric.worker_id,
            "correlation_id": metric.correlation_id,
            "trace_id": metric.trace_id,
        }

        for key, value in metric.labels.items():
            row[
                f"label_{key}"
            ] = value

        if metric.metadata:
            for key, value in metric.metadata.items():
                row[
                    f"metadata_{key}"
                ] = value

        return row

    def to_rows(
        self,
        *,
        metrics: tuple[
            TelemetryMetric,
            ...,
        ],
    ) -> tuple[
        dict[
            str,
            Any,
        ],
        ...,
    ]:
        return tuple(
            self.to_row(
                metric=metric,
            )
            for metric in metrics
        )