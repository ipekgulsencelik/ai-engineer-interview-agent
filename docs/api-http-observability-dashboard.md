# HTTP request tracing and Grafana/Prometheus dashboards

This increment extends the *existing* opt-in dataset monitoring OpenTelemetry
runtime with HTTP request tracing and server metrics. The FastAPI application
is unchanged when telemetry is not configured.

## SOLID / Clean Architecture

- `HTTPServerTelemetryPort`: small application-layer recording interface.
- `SafeHTTPServerTelemetry`: ensures exporter failures cannot change an
  otherwise successful HTTP request or obscure an application exception.
- `HTTPRequestObservabilityMiddleware`: pure ASGI adapter; no dependency
  on an OpenTelemetry SDK or Prometheus client. It instruments HTTP scopes
  only and does not buffer/inspect body or response content.
- `OpenTelemetryHTTPServerTelemetry`: infrastructure SDK implementation,
  taking explicit meter, tracer and **bounded route-template allowlist**.
- `DatasetTelemetryRuntime.http_server_telemetry(...)`: constructs the
  HTTP adapter using the *existing providers and isolated registry*.
- `create_app(http_telemetry=...)` or
  `instrument_http_app(app, telemetry=...)`: explicit composition-root DI.

The pre-existing monitoring/dispatch `DatasetTelemetryPort` is left
unchanged. HTTP and background worker metrics may share one runtime.

## Metric contract

| OpenTelemetry instrument | Type | Allowed dimensions |
| --- | --- | --- |
| `http_server_requests` | monotonic counter | `method`, `route`, `status_class` |
| `http_server_request_duration` | histogram, seconds | `method`, `route`, `status_class` |

The Prometheus exporter renders the corresponding counter and histogram
series, used by the dashboard:
`http_server_requests_total` and
`http_server_request_duration_seconds_bucket`.

Only static declared **route templates** (e.g. `/items/{item_id}`) are
included, never `/items/123`; unknown routes are aggregated under
`unmatched`. HTTP verbs are one of GET/POST/PUT/PATCH/DELETE/HEAD/OPTIONS
or OTHER. Status labels are only `2xx`, `3xx`, `4xx`, `5xx`.
The route allowlist is capped at 128 registered routes. If more routes
are added, expand this limit only after evaluating cardinality budgets.

Trace spans are `http.server.request` with only bounded
`http.request.method` and `http.route` attributes. The SDK disables
exception recording and exception-status inference, so it never includes
a sensitive traceback in exported span events. Middleware marks
unhandled exceptions as `5xx` and re-raises without changing responses.

**Not recorded:** Authorization headers, cookies, URL query values, raw
paths, request/response bodies, candidate answers, client IPs, exception
text, dataset IDs, user IDs or arbitrary labels.

## How to enable for FastAPI (opt-in)

Install optional dependencies (do not edit the core frozen lock):

```bash
uv pip install --python .venv/bin/python -r requirements-observability.txt
```

Configure the application **before serving the first request**:

```python
from prometheus_client import start_http_server

from src.api.app import (
    create_app,
    instrument_http_app,
    registered_route_templates,
)
from src.infrastructure.telemetry.runtime import create_prometheus_runtime

runtime = create_prometheus_runtime(
    service_name="ai-engineer-interview-agent",
    # Optional HTTPS OTLP tracing collector:
    # otlp_traces_endpoint="https://otel.example.com/v1/traces",
)

app = create_app()
http_telemetry = runtime.http_server_telemetry(
    route_templates=registered_route_templates(app),
)
instrument_http_app(app, telemetry=http_telemetry)

# Expose the *isolated* Prometheus registry on loopback only by default.
start_http_server(9464, addr="127.0.0.1", registry=runtime.registry)

# Host process must call runtime.shutdown() during graceful termination.
```

Use the application's startup/lifespan composition to own `runtime` and
shutdown. The above example demonstrates wiring; it is not an automated
background service, an authorization layer or a deployment entrypoint.

The middleware cannot be added once the FastAPI application has begun
serving requests. Existing `src.api.app.app` remains uninstrumented until
the deployment chooses the opt-in composition.

For multiple uvicorn worker processes, a single local Prometheus pull
registry does **not** aggregate across workers. Deploy one scrape target
per process or export telemetry to an OTLP Collector with multi-process
support. Do not treat a single worker scrape as fleet-wide statistics.

## Dashboard and alert rules

Import `ops/observability/grafana/ai-interview-http-dataset-dashboard.json`
into Grafana, selecting your Prometheus datasource. It displays:
HTTP requests/sec, server 5xx ratio, overall and per-route p95 latency,
per-route request volume, and dataset operation outcomes. The JSON uses
supported Prometheus datasource references but does **not** create a Grafana
server or provision credentials.

The existing `ops/observability/prometheus-example.yml` scrapes a
loopback registry at port 9464. Example warning rules in
`ops/observability/prometheus-rules-example.yml` add a 5xx ratio
(5%) and p95 latency (2 seconds) threshold. These are **illustrative**,
not production-specific SLOs. When the denominator is zero, no
request-series exists and alerts may not fire; add proper availability
monitoring and low-traffic handling before production use.

Metrics server access should be limited by firewall, service mesh or
authenticated ingress. Never expose metrics publicly by default.

## Testing and release expectations

- Default CI: Ruff + Pyright + the entire Pytest suite (HTTP behavior,
  404/405, streaming responses, 5xx, exporter failures and opt-in wiring).
- SDK CI: real OpenTelemetry counters, histograms, privacy-safe spans and
  Prometheus exposition, and a JSON dashboard contract test.
- PostgreSQL/Alembic CI must remain green; HTTP instrumentation does not
  modify persistence, transactional outbox, or database migrations.

Further Enterprise-Level work still includes: real OTLP Collector deployment,
multi-worker service topology, secured ingress, readiness vs liveness,
distributed trace propagation policy, privacy review, SLO baselines,
production dashboards and alerts, load tests, and backup/disaster recovery.
