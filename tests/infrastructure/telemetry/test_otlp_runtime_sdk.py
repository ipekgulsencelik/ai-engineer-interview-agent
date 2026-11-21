"""Real loopback OTLP/HTTP export and explicit transport policy tests."""

from __future__ import annotations

import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest

pytest.importorskip("opentelemetry.exporter.otlp.proto.http.metric_exporter")
pytest.importorskip("opentelemetry.exporter.otlp.proto.http.trace_exporter")

from src.infrastructure.telemetry.runtime import create_otlp_runtime  # noqa: E402


@pytest.mark.parametrize(
    "url",
    [
        "http://example.com:4318",
        "http://otel-collector:4318",
        "http://localhost:4318/private",
        "https://user:secret@host:4318",
        "https://host:4318/v1/metrics",
        "ftp://host:4318",
        "http://127.0.0.1:4318?token=secret",
        "https://host:bogus",
    ],
)
def test_transport_rejects_unapproved_or_malformed_endpoints(
    url: str,
) -> None:
    with pytest.raises(ValueError):
        create_otlp_runtime(
            service_name="test",
            collector_endpoint=url,
        )


def test_explicit_insecure_local_never_allows_arbitrary_host() -> None:
    with pytest.raises(ValueError, match="restricted"):
        create_otlp_runtime(
            service_name="test",
            collector_endpoint="http://untrusted.example:4318",
            allow_insecure_local=True,
        )


@pytest.mark.parametrize(
    "interval", [0, 999, 300001, True]
)
def test_export_interval_rejects_invalid_values(interval: int) -> None:
    with pytest.raises(ValueError, match="export_interval"):
        create_otlp_runtime(
            service_name="test",
            collector_endpoint="https://otel.example:4318",
            export_interval_millis=interval,
        )


def test_metrics_and_traces_are_exported_to_distinct_otlp_paths() -> None:
    seen: list[tuple[str, bytes]] = []

    class Receiver(BaseHTTPRequestHandler):
        def do_POST(self) -> None:
            length = int(self.headers["Content-Length"])
            payload = self.rfile.read(length)
            seen.append((self.path, payload))
            self.send_response(200)
            self.end_headers()

        def log_message(self, fmt: str, *args: object) -> None:
            return

    server = ThreadingHTTPServer(("127.0.0.1", 0), Receiver)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    runtime = create_otlp_runtime(
        service_name="interview-test",
        collector_endpoint=f"http://127.0.0.1:{server.server_port}",
        allow_insecure_local=True,
        export_interval_millis=300000,
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
                duration_seconds=0.08,
            )
        assert runtime.meter_provider.force_flush(timeout_millis=5000)
        assert runtime.tracer_provider.force_flush(timeout_millis=5000)
        assert any(path == "/v1/metrics" and body for path, body in seen)
        assert any(path == "/v1/traces" and body for path, body in seen)
        assert all(
            b"SECRET-CANDIDATE" not in body for _path, body in seen
        )
        assert runtime.registry is None
    finally:
        runtime.shutdown()
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
