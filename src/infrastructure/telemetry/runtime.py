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
from src.infrastructure.telemetry.otel_http_server_telemetry import (
    OpenTelemetryHTTPServerTelemetry,
)


@dataclass(slots=True)
class DatasetTelemetryRuntime:
    """A single-process SDK runtime with deliberate shutdown ownership."""

    telemetry: OpenTelemetryDatasetTelemetry
    meter_provider: Any
    tracer_provider: Any
    registry: Any

    def http_server_telemetry(
        self, *, route_templates: frozenset[str]
    ) -> OpenTelemetryHTTPServerTelemetry:
        """Share the same meter/tracer providers without global mutations."""
        return OpenTelemetryHTTPServerTelemetry(
            meter=self.meter_provider.get_meter("http.server"),
            tracer=self.tracer_provider.get_tracer("http.server"),
            route_templates=route_templates,
        )

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


def create_otlp_runtime(
    *,
    service_name: str,
    collector_endpoint: str,
    allow_insecure_local: bool = False,
    export_interval_millis: int = 15000,
    headers: dict[str, str] | None = None,
) -> DatasetTelemetryRuntime:
    """Build opt-in OTLP HTTP metrics+traces with a single injected SDK.

    HTTPS is mandatory, except explicit opt-in for localhost or the isolated
    Docker Compose hostname "otel-collector". Never mutates global providers.
    A metric push reader supports separate app worker processes; the collector
    is responsible for fleet-level aggregation and forwarding.
    """
    from urllib.parse import urlsplit

    if not isinstance(service_name, str) or not service_name.strip():
        raise ValueError("service_name must be non-empty")
    if type(export_interval_millis) is not int or not (
        1000 <= export_interval_millis <= 300000
    ):
        raise ValueError("export_interval_millis must be in [1000, 300000]")
    if type(allow_insecure_local) is not bool:
        raise ValueError("allow_insecure_local must be boolean")
    if not isinstance(collector_endpoint, str):
        raise ValueError("collector_endpoint must be URL")
    try:
        endpoint = urlsplit(collector_endpoint)
        port = endpoint.port
    except ValueError as exc:
        raise ValueError("collector_endpoint must have valid port") from exc
    if (
        endpoint.scheme not in ("https", "http")
        or not endpoint.hostname
        or port is None
        or endpoint.username is not None
        or endpoint.password is not None
        or endpoint.path not in ("", "/")
        or endpoint.query
        or endpoint.fragment
    ):
        raise ValueError(
            "collector_endpoint must be a scheme, host and port with no credentials"
        )
    if endpoint.scheme == "http" and not (
        allow_insecure_local
        and endpoint.hostname in ("localhost", "127.0.0.1", "::1", "otel-collector")
    ):
        raise ValueError(
            "plain HTTP OTLP is restricted to explicitly approved local hosts"
        )
    if headers is not None and (
        not isinstance(headers, dict)
        or any(
            not isinstance(key, str) or not key.strip()
            or not isinstance(value, str)
            for key, value in headers.items()
        )
    ):
        raise ValueError("headers must be a mapping of nonempty names and values")

    try:
        sdk_metrics = importlib.import_module("opentelemetry.sdk.metrics")
        sdk_trace = importlib.import_module("opentelemetry.sdk.trace")
        sdk_resource = importlib.import_module("opentelemetry.sdk.resources")
        sdk_metric_export = importlib.import_module(
            "opentelemetry.sdk.metrics.export"
        )
        sdk_trace_export = importlib.import_module(
            "opentelemetry.sdk.trace.export"
        )
        otlp_metrics = importlib.import_module(
            "opentelemetry.exporter.otlp.proto.http.metric_exporter"
        )
        otlp_trace = importlib.import_module(
            "opentelemetry.exporter.otlp.proto.http.trace_exporter"
        )
    except ImportError as exc:
        raise RuntimeError(
            "Install optional requirements-observability.txt for OTLP"
        ) from exc

    base_url = collector_endpoint.rstrip("/")
    resource = sdk_resource.Resource.create({"service.name": service_name})
    meter_reader = sdk_metric_export.PeriodicExportingMetricReader(
        otlp_metrics.OTLPMetricExporter(
            endpoint=f"{base_url}/v1/metrics",
            timeout=5,
            headers=headers,
        ),
        export_interval_millis=export_interval_millis,
        export_timeout_millis=5000,
    )
    meter_provider = sdk_metrics.MeterProvider(
        resource=resource,
        metric_readers=[meter_reader],
    )
    tracer_provider = sdk_trace.TracerProvider(resource=resource)
    try:
        tracer_provider.add_span_processor(
            sdk_trace_export.BatchSpanProcessor(
                otlp_trace.OTLPSpanExporter(
                    endpoint=f"{base_url}/v1/traces",
                    timeout=5,
                    headers=headers,
                )
            )
        )
        return DatasetTelemetryRuntime(
            telemetry=OpenTelemetryDatasetTelemetry(
                meter=meter_provider.get_meter("dataset.observability"),
                tracer=tracer_provider.get_tracer("dataset.observability"),
            ),
            meter_provider=meter_provider,
            tracer_provider=tracer_provider,
            registry=None,
        )
    except Exception:
        meter_provider.shutdown()
        tracer_provider.shutdown()
        raise
