# OpenTelemetry + Prometheus — dataset monitoring instrumentation

This increment instruments the **dataset monitoring coordinator** and the
**leased alert dispatcher**, retaining the same SOLID / Clean Architecture
ports and behavior on the default installation.

## What is instrumented

- `dataset_operations`: an OpenTelemetry monotonic counter grouped by
  exactly two bounded attributes: `activity` (`monitor` / `dispatch`)
  and `outcome` (`healthy`, `warning`, `critical`, `error`,
  `delivered`, `retry`, `dead_letter`). Prometheus appends counter
  naming conventions during exposition.
- `dataset_operation_duration`: histogram in seconds, only
  `activity` is attached.
- `dataset.monitor` and `dataset.dispatch`: optional trace spans.
  **No dataset_id, run_id, worker_id, alert_id, request body, sample
  content, exception message, tokens, or URLs** are recorded as span
  attributes or metric labels.

The existing `OpenTelemetryMetricClient` and `OpenTelemetryExporter`
in `src/evaluation/reporting` remain separate: they export individual
evaluation report metrics. This module provides **runtime operation
instrumentation** for dataset monitoring and leased alert delivery, without
modifying or replacing that exporter.

## SOLID / DI architecture

`DatasetTelemetryPort` is a narrow protocol in the application/domain
layer, implemented by `OpenTelemetryDatasetTelemetry` in infrastructure.
`SafeDatasetTelemetry` isolates SDK failures so an observability outage
cannot turn an already committed monitoring operation or acknowledged
alert into an apparent business failure. With no injected telemetry,
`NoopDatasetTelemetry` keeps existing behavior unchanged.

The SDK runtime builder does not mutate global provider state or open
network listeners. The composition root chooses when to create providers,
bind a scrape endpoint, and release resources.

## Install and configure

The default Python application and frozen `uv.lock` need no extra package.
For deployment or local observability integration:

```bash
uv pip install --python .venv/bin/python -r requirements-observability.txt
```

Example composition for **one process**:

```python
from prometheus_client import start_http_server

from src.evaluation.dataset.observability import (
    DatasetObservabilityCoordinator,
    DatasetObservabilityMonitor,
    LeasedDatasetAlertDispatcher,
)
from src.infrastructure.telemetry.runtime import create_prometheus_runtime

runtime = create_prometheus_runtime(
    service_name="ai-engineer-interview-dataset-worker",
    # Optional HTTPS OTLP collector:
    # otlp_traces_endpoint="https://collector.example.org/v1/traces",
)
start_http_server(
    port=9464,
    addr="127.0.0.1",
    registry=runtime.registry,
)

coordinator = DatasetObservabilityCoordinator(
    monitor=DatasetObservabilityMonitor(),
    store=monitoring_repository,
    telemetry=runtime.telemetry,
)
dispatcher = LeasedDatasetAlertDispatcher(
    outbox=leased_alert_outbox,
    sender=alert_sender,
    worker_id="worker-1",
    telemetry=runtime.telemetry,
)

# The host application owns process startup, monitoring job scheduling,
# HTTP scrape access controls, and graceful shutdown:
# runtime.shutdown()
```

Here `monitoring_repository`, `leased_alert_outbox`, and
`alert_sender` are existing explicit composition-root dependencies;
this is an integration example rather than a runnable standalone script.

The Prometheus example files under `ops/observability` show scrape targets
and basic alert rules. **These are examples, not tuned operational SLOs.**
Prometheus ingestion, dashboard creation, and alert delivery to production
incident platforms require separate deployment configuration.

## Privacy and operational constraints

1. **Cardinality discipline:** only fixed enumerations become metric labels,
   never user-controlled or dataset-specific values.
2. **Fail-safe telemetry:** business errors propagate; telemetry SDK/reader
   failures are caught at the port boundary and logged without exception
   details. A telemetry outage does not falsely acknowledge a failed write.
3. **No exception recording in spans:** the OTel adapter disables automatic
   exception event capture and exception-derived span status, because SDK
   exception strings can contain source data.
4. **Scrape exposure:** the example binds to `127.0.0.1`. For cross-host
   scraping, use authenticated networking / ingress rules. Do not expose
   unauthenticated `/metrics` to the public internet.
5. **OTLP traces:** trace export is opt-in via an **HTTPS** endpoint and the
   SDK's batch processor. Without that option, traces have no exporter and
   are not shipped to an external backend.
6. **Single-process Prometheus limit:** the OpenTelemetry Python Prometheus
   exporter does not support multiple Python worker processes sharing one
   scrape target. For multi-process services, prefer an OTLP Collector path
   with a compatible metrics backend, or a separate per-process scrape
   architecture; do not assume this adapter aggregates all workers.
7. **Lifecycle:** call `runtime.shutdown()` once during host shutdown to
   flush/shutdown providers. No background worker or HTTP server is
   started automatically.
8. **Deployment:** this PR does **not** provide HTTP request tracing,
   PostgreSQL query instrumentation, production alert routing, RBAC,
   multi-tenancy, dashboards, on-call SLOs, or audited permission gates.

## CI verification

The standard CI job runs Ruff, Pyright and all default tests without
installing optional SDK dependencies. A separate lightweight job installs
`requirements-observability.txt` and checks real SDK counters, histograms,
span redaction and Prometheus text exposition with an isolated registry.
Tests also verify successful business persistence if a telemetry backend
raises, and that business errors are reported without exposing private IDs.

This is a **production-oriented observability integration**, not proof of
overall Enterprise-Level availability or security compliance.
