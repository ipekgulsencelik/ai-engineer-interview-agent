from __future__ import annotations

from src.evaluation.reporting.entities.telemetry_metric import (
    TelemetryMetric,
)


class TelemetryAttributeBuilder:
    """
    Builds OpenTelemetry attribute payloads.
    """

    def __init__(
        self,
        *,
        service_name: str,
    ) -> None:
        self._service_name = service_name

    def build(
        self,
        *,
        metric: TelemetryMetric,
    ) -> dict[
        str,
        str,
    ]:
        attributes = {
            "service.name": self._service_name,
            "metric.id": metric.metric_id,
            "metric.source": metric.source,
            "metric.recorded_at": (
                metric.recorded_at.isoformat()
            ),
            **metric.labels,
        }

        self._add_optional(
            attributes=attributes,
            key="tenant.id",
            value=metric.tenant_id,
        )

        self._add_optional(
            attributes=attributes,
            key="experiment.id",
            value=metric.experiment_id,
        )

        self._add_optional(
            attributes=attributes,
            key="run.id",
            value=metric.run_id,
        )

        self._add_optional(
            attributes=attributes,
            key="report.id",
            value=metric.report_id,
        )

        self._add_optional(
            attributes=attributes,
            key="artifact.id",
            value=metric.artifact_id,
        )

        self._add_optional(
            attributes=attributes,
            key="worker.id",
            value=metric.worker_id,
        )

        self._add_optional(
            attributes=attributes,
            key="correlation.id",
            value=metric.correlation_id,
        )

        self._add_optional(
            attributes=attributes,
            key="trace.id",
            value=metric.trace_id,
        )

        if metric.metadata:
            for key, value in metric.metadata.items():
                attributes[
                    f"metadata.{key}"
                ] = value

        return attributes

    @staticmethod
    def _add_optional(
        *,
        attributes: dict[
            str,
            str,
        ],
        key: str,
        value: str | None,
    ) -> None:
        if value is None:
            return

        attributes[
            key
        ] = value