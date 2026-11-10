"""Real SDK and Prometheus registry tests when optional packages are installed."""

from __future__ import annotations

import pytest

pytest.importorskip("opentelemetry.sdk.metrics")

from src.infrastructure.telemetry.otel_dataset_telemetry import (  # noqa: E402
    OpenTelemetryDatasetTelemetry,
)
from src.infrastructure.telemetry.runtime import (  # noqa: E402
    create_prometheus_runtime,
)


def test_real_sdk_exports_counter_histogram_and_private_tracing() -> None:
    from opentelemetry.sdk.metrics import MeterProvider
    from opentelemetry.sdk.metrics.export import InMemoryMetricReader
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import SimpleSpanProcessor
    from opentelemetry.sdk.trace.export.in_memory_span_exporter import (
        InMemorySpanExporter,
    )

    reader = InMemoryMetricReader()
    meters = MeterProvider(metric_readers=[reader])
    spans = InMemorySpanExporter()
    traces = TracerProvider()
    traces.add_span_processor(SimpleSpanProcessor(spans))
    adapter = OpenTelemetryDatasetTelemetry(
        meter=meters.get_meter("dataset.observability.test"),
        tracer=traces.get_tracer("dataset.observability.test"),
    )
    try:
        with adapter.span(activity="monitor"):
            adapter.count(activity="monitor", outcome="healthy")
            adapter.duration(activity="monitor", seconds=0.25)

        data = reader.get_metrics_data()
        assert data is not None
        points = {
            metric.name: metric.data.data_points
            for resource in data.resource_metrics
            for scope in resource.scope_metrics
            for metric in scope.metrics
        }
        assert "dataset_operations" in points
        assert "dataset_operation_duration" in points
        assert points["dataset_operations"][0].value == 1
        assert points["dataset_operation_duration"][0].count == 1
        emitted = spans.get_finished_spans()
        assert len(emitted) == 1
        assert emitted[0].name == "dataset.monitor"
        assert emitted[0].attributes == {"activity": "monitor"}
        assert not emitted[0].events
    finally:
        meters.shutdown()
        traces.shutdown()


@pytest.mark.parametrize(
    ("activity", "outcome", "amount"),
    [
        ("private-dataset-id", "healthy", 1),
        ("monitor", "private-sample", 1),
        ("monitor", "healthy", -1),
    ],
)
def test_real_sdk_rejects_unbounded_telemetry_labels(
    activity: str, outcome: str, amount: int
) -> None:
    from opentelemetry.sdk.metrics import MeterProvider
    from opentelemetry.sdk.trace import TracerProvider

    meters = MeterProvider()
    traces = TracerProvider()
    adapter = OpenTelemetryDatasetTelemetry(
        meter=meters.get_meter("test"),
        tracer=traces.get_tracer("test"),
    )
    try:
        with pytest.raises(ValueError):
            adapter.count(activity=activity, outcome=outcome, amount=amount)
    finally:
        meters.shutdown()
        traces.shutdown()


def test_spans_do_not_capture_exception_messages() -> None:
    from opentelemetry.sdk.metrics import MeterProvider
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import SimpleSpanProcessor
    from opentelemetry.sdk.trace.export.in_memory_span_exporter import (
        InMemorySpanExporter,
    )

    meters = MeterProvider()
    traces = TracerProvider()
    exporter = InMemorySpanExporter()
    traces.add_span_processor(SimpleSpanProcessor(exporter))
    adapter = OpenTelemetryDatasetTelemetry(
        meter=meters.get_meter("test"),
        tracer=traces.get_tracer("test"),
    )
    try:
        with pytest.raises(RuntimeError, match="private candidate data"):
            with adapter.span(activity="dispatch"):
                raise RuntimeError("private candidate data")
        span = exporter.get_finished_spans()[0]
        assert span.name == "dataset.dispatch"
        assert span.events == ()
        assert "private candidate data" not in repr(span.attributes)
    finally:
        meters.shutdown()
        traces.shutdown()


def test_prometheus_runtime_uses_isolated_registry_not_global_state() -> None:
    from prometheus_client import CollectorRegistry, generate_latest

    registry = CollectorRegistry(auto_describe=True)
    runtime = create_prometheus_runtime(
        service_name="dataset-monitoring-tests",
        registry=registry,
    )
    try:
        runtime.telemetry.count(
            activity="dispatch", outcome="delivered", amount=2
        )
        runtime.telemetry.duration(activity="dispatch", seconds=0.12)
        payload = generate_latest(runtime.registry).decode()
        assert "dataset_operations" in payload
        assert "dataset_operation_duration" in payload
        assert 'activity="dispatch"' in payload
        assert 'outcome="delivered"' in payload
        assert "dataset-id" not in payload
    finally:
        runtime.shutdown()


def test_prometheus_runtime_rejects_non_https_otlp_endpoint() -> None:
    with pytest.raises(ValueError, match="HTTPS"):
        create_prometheus_runtime(
            service_name="test",
            otlp_traces_endpoint="http://collector.local/v1/traces",
        )
