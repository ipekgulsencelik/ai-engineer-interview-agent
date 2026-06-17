from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from src.evaluation.reporting.validators.telemetry_metric_validator import (
    TelemetryMetricValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class TelemetryMetric:
    """
    Immutable telemetry metric.

    Represents an observability metric emitted from
    evaluation runs, report generation pipelines,
    dashboard refreshes, delivery workflows,
    tracking integrations, and distributed workers.

    Designed to align with OpenTelemetry /
    Prometheus-style metric collection.
    """

    metric_id: str

    metric_name: str

    metric_value: float

    unit: str

    source: str

    recorded_at: datetime

    labels: dict[
        str,
        str,
    ]

    tenant_id: str | None = None

    experiment_id: str | None = None

    run_id: str | None = None

    report_id: str | None = None

    artifact_id: str | None = None

    worker_id: str | None = None

    correlation_id: str | None = None

    trace_id: str | None = None

    metadata: dict[
        str,
        str,
    ] | None = None

    def __post_init__(
        self,
    ) -> None:
        TelemetryMetricValidator.validate(
            metric_id=self.metric_id,
            metric_name=self.metric_name,
            metric_value=self.metric_value,
            unit=self.unit,
            source=self.source,
            recorded_at=self.recorded_at,
            labels=self.labels,
            tenant_id=self.tenant_id,
            experiment_id=self.experiment_id,
            run_id=self.run_id,
            report_id=self.report_id,
            artifact_id=self.artifact_id,
            worker_id=self.worker_id,
            correlation_id=self.correlation_id,
            trace_id=self.trace_id,
            metadata=self.metadata,
        )

    @property
    def has_labels(
        self,
    ) -> bool:
        return bool(
            self.labels,
        )

    @property
    def has_tenant(
        self,
    ) -> bool:
        return (
            self.tenant_id
            is not None
        )

    @property
    def has_experiment(
        self,
    ) -> bool:
        return (
            self.experiment_id
            is not None
        )

    @property
    def has_run(
        self,
    ) -> bool:
        return (
            self.run_id
            is not None
        )

    @property
    def has_report(
        self,
    ) -> bool:
        return (
            self.report_id
            is not None
        )

    @property
    def has_artifact(
        self,
    ) -> bool:
        return (
            self.artifact_id
            is not None
        )

    @property
    def has_worker(
        self,
    ) -> bool:
        return (
            self.worker_id
            is not None
        )

    @property
    def has_correlation(
        self,
    ) -> bool:
        return (
            self.correlation_id
            is not None
        )

    @property
    def has_trace(
        self,
    ) -> bool:
        return (
            self.trace_id
            is not None
        )

    @property
    def has_metadata(
        self,
    ) -> bool:
        return bool(
            self.metadata,
        )

    @property
    def metric_key(
        self,
    ) -> str:
        if not self.labels:
            return self.metric_name

        label_part = ",".join(
            f"{key}={value}"
            for key, value
            in sorted(
                self.labels.items(),
            )
        )

        return (
            f"{self.metric_name}"
            f"{{{label_part}}}"
        )

    @property
    def is_counter(
        self,
    ) -> bool:
        return (
            self.unit
            == "count"
        )

    @property
    def is_percentage(
        self,
    ) -> bool:
        return (
            self.unit
            in {
                "%",
                "percent",
                "percentage",
            }
        )

    @property
    def is_latency_metric(
        self,
    ) -> bool:
        return (
            "latency"
            in self.metric_name.lower()
        )

    @property
    def is_error_metric(
        self,
    ) -> bool:
        return (
            "error"
            in self.metric_name.lower()
        )