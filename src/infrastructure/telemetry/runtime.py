"""Explicit opt-in OpenTelemetry/Prometheus runtime composition.

Prometheus is a pull-based exporter. The caller owns HTTP exposure and
process lifecycle; this module never binds sockets or sets global providers.
"""

from __future__ import annotations

import importlib
from dataclasses import dataclass
from typing import Any

from src.infrastructure.telemetry.otel_dataset_telemetry import (
    OpenTelemetryDatasetTelemetry,
)


@dataclass(slots=True)
class DatasetTelemetryRuntime:
    """A single-process SDK runtime with deliberate shutdown ownership."""

    telemetry: OpenTelemetryDatasetTelemetry
    meter_provider: Any
    tracer_provider: Any
    registry: Any

    def shutdown(self) -> None:
        # OTel providers manage reader/span processor lifetimes.
        self.meter_provider.shutdown()
        self.tracer_provider.shutdown()


def create_prometheus_runtime(
    *,
    service_name: str,
    registry: Any = None,
    otlp_traces_endpoint: str | None = None,
) -> DatasetTelemetryRuntime:
    """Build local pull-metrics and optional HTTPS OTLP trace export."""
    if not isinstance(service_name, str) or not service_name.strip():
        raise ValueError("service_name must be a non-empty string")
    if otlp_traces_endpoint is not None and not (
        isinstance(otlp_traces_endpoint, str)
        and otlp_traces_endpoint.startswith("https://")
    ):
        raise ValueError("OTLP traces endpoint must use HTTPS")
    try:
        prom_client = importlib.import_module("prometheus_client")
        prom_exporter = importlib.import_module(
            "opentelemetry.exporter.prometheus"
        )
        sdk_metrics = importlib.import_module("opentelemetry.sdk.metrics")
        sdk_trace = importlib.import_module("opentelemetry.sdk.trace")
        sdk_resource = importlib.import_module("opentelemetry.sdk.resources")
    except ImportError as exc:
        raise RuntimeError(
            "Install the optional requirements-observability.txt"
        ) from exc

    metric_registry = (
        registry if registry is not None
        else prom_client.CollectorRegistry(auto_describe=True)
    )
    reader = prom_exporter.PrometheusMetricReader(
        registry=metric_registry,
        scope_info_enabled=False,
        resource_attribute_filter=lambda _name: False,
    )
    resource = sdk_resource.Resource.create(
        {"service.name": service_name}
    )
    meter_provider = sdk_metrics.MeterProvider(
        resource=resource,
        metric_readers=[reader],
    )
    tracer_provider = sdk_trace.TracerProvider(resource=resource)
    if otlp_traces_endpoint is not None:
        try:
            processor_module = importlib.import_module(
                "opentelemetry.sdk.trace.export"
            )
            otlp_module = importlib.import_module(
                "opentelemetry.exporter.otlp.proto.http.trace_exporter"
            )
        except ImportError as exc:
            meter_provider.shutdown()
            tracer_provider.shutdown()
            raise RuntimeError(
                "Install OTLP trace exporter requirements"
            ) from exc
        processor = processor_module.BatchSpanProcessor(
            otlp_module.OTLPSpanExporter(endpoint=otlp_traces_endpoint)
        )
        tracer_provider.add_span_processor(processor)

    telemetry = OpenTelemetryDatasetTelemetry(
        meter=meter_provider.get_meter("dataset.observability"),
        tracer=tracer_provider.get_tracer("dataset.observability"),
    )
    return DatasetTelemetryRuntime(
        telemetry=telemetry,
        meter_provider=meter_provider,
        tracer_provider=tracer_provider,
        registry=metric_registry,
    )
