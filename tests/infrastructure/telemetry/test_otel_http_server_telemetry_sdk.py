"""Real OpenTelemetry metrics and spans for HTTP request instrumentation."""

from __future__ import annotations

import pytest

pytest.importorskip("opentelemetry.sdk.metrics")

from src.infrastructure.telemetry.otel_http_server_telemetry import (  # noqa: E402
    OpenTelemetryHTTPServerTelemetry,
)


def _meters():
    from opentelemetry.sdk.metrics import MeterProvider
    from opentelemetry.sdk.metrics.export import InMemoryMetricReader
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import SimpleSpanProcessor
    from opentelemetry.sdk.trace.export.in_memory_span_exporter import (
        InMemorySpanExporter,
    )

    reader = InMemoryMetricReader()
    provider = MeterProvider(metric_readers=[reader])
    spans = InMemorySpanExporter()
    tracer_provider = TracerProvider()
    tracer_provider.add_span_processor(SimpleSpanProcessor(spans))
    sdk = OpenTelemetryHTTPServerTelemetry(
        meter=provider.get_meter("http.observability.test"),
        tracer=tracer_provider.get_tracer("http.observability.test"),
        route_templates=frozenset({"/items/{item_id}", "/api/v1/health/"}),
    )
    return sdk, reader, provider, tracer_provider, spans


def test_real_sdk_counter_histogram_and_sanitized_span() -> None:
    sdk, reader, meters, traces, spans = _meters()
    try:
        with sdk.span(method="GET", route="/items/{item_id}"):
            sdk.observe(
                method="GET", route="/items/{item_id}",
                status_class="2xx", duration_seconds=0.08,
            )
        data = reader.get_metrics_data()
        assert data is not None
        metrics = {
            metric.name: metric
            for group in data.resource_metrics
            for scope in group.scope_metrics
            for metric in scope.metrics
        }
        assert metrics["http_server_requests"].data.data_points[0].value == 1
        duration_points = metrics[
            "http_server_request_duration"
        ].data.data_points
        assert duration_points[0].count == 1
        attrs = dict(duration_points[0].attributes)
        assert attrs == {
            "method": "GET",
            "route": "/items/{item_id}",
            "status_class": "2xx",
        }
        span = spans.get_finished_spans()[0]
        assert span.name == "http.server.request"
        assert span.attributes == {
            "http.request.method": "GET",
            "http.route": "/items/{item_id}",
        }
        assert not span.events
        assert "secret-user" not in repr(data)
    finally:
        meters.shutdown()
        traces.shutdown()


@pytest.mark.parametrize(
    ("method", "route", "status"),
    [
        ("TOKEN-PRIVATE", "/items/{item_id}", "2xx"),
        ("GET", "/items/SECRET-USER", "2xx"),
        ("GET", "/items/{item_id}", "secret-status"),
    ],
)
def test_rejects_high_cardinality_labels(
    method: str, route: str, status: str
) -> None:
    sdk, _reader, meters, traces, _spans = _meters()
    try:
        with pytest.raises(ValueError):
            sdk.observe(
                method=method, route=route, status_class=status,
                duration_seconds=0.1,
            )
    finally:
        meters.shutdown()
        traces.shutdown()


def test_sdk_disables_span_exception_capture() -> None:
    sdk, _reader, meters, traces, spans = _meters()
    try:
        with pytest.raises(RuntimeError, match="private candidate answer"):
            with sdk.span(method="GET", route="/api/v1/health/"):
                raise RuntimeError("private candidate answer")
        span = spans.get_finished_spans()[0]
        assert not span.events
        assert "private candidate answer" not in repr(span.attributes)
    finally:
        meters.shutdown()
        traces.shutdown()


def test_real_prometheus_exposition_for_dashboard_queries() -> None:
    pytest.importorskip("prometheus_client")
    pytest.importorskip("opentelemetry.exporter.prometheus")
    from prometheus_client import CollectorRegistry, generate_latest

    from src.infrastructure.telemetry.runtime import create_prometheus_runtime

    registry = CollectorRegistry(auto_describe=True)
    runtime = create_prometheus_runtime(
        service_name="ai-engineer-interview-http",
        registry=registry,
    )
    try:
        sdk = runtime.http_server_telemetry(
            route_templates=frozenset({"/api/v1/health/"})
        )
        with sdk.span(method="GET", route="/api/v1/health/"):
            sdk.observe(
                method="GET",
                route="/api/v1/health/",
                status_class="2xx",
                duration_seconds=0.1,
            )
        payload = generate_latest(registry).decode()
        assert "http_server_requests_total" in payload
        assert "http_server_request_duration_seconds_bucket" in payload
        assert 'route="/api/v1/health/"' in payload
        assert 'status_class="2xx"' in payload
        assert "PRIVATE-TOKEN" not in payload
    finally:
        runtime.shutdown()


def test_route_allowlist_is_bounded_and_validated() -> None:
    sdk, _reader, meters, traces, _spans = _meters()
    try:
        with pytest.raises(ValueError, match="route_templates"):
            OpenTelemetryHTTPServerTelemetry(
                meter=meters.get_meter("other"),
                tracer=traces.get_tracer("other"),
                route_templates=frozenset({"SECRET-ID"}),
            )
        with pytest.raises(ValueError, match="route_templates"):
            OpenTelemetryHTTPServerTelemetry(
                meter=meters.get_meter("other"),
                tracer=traces.get_tracer("other"),
                route_templates=frozenset(
                    f"/endpoint/{n}" for n in range(129)
                ),
            )
        with pytest.raises(ValueError, match="duration_seconds"):
            sdk.observe(
                method="GET", route="/items/{item_id}",
                status_class="2xx", duration_seconds=float("nan"),
            )
    finally:
        meters.shutdown()
        traces.shutdown()
