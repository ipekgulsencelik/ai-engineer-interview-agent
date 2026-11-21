# Reference deployment: OTLP Collector, Tempo, Prometheus, Grafana and SLO alerts

This opt-in, single-host **reference stack** extends PR #31's HTTP tracing
and dashboards. It is an operational foundation, **not** a certified HA,
multi-tenant, independently security-audited production deployment.

## Architecture and data flow

- Python FastAPI worker `create_otlp_runtime` / `build_otel_app` ->
  **OTLP HTTP push** for metrics and traces to the OpenTelemetry Collector.
- Collector -> **Prometheus exporter** for metrics, scraped privately by
  Prometheus; Collector -> **Tempo** OTLP gRPC for traces.
- Prometheus -> SLO recording/alert rules -> **Alertmanager** ->
  operator-controlled authenticated incident webhook.
- **Grafana** uses file provisioning for immutable data sources and dashboard.

Unlike the old Python Prometheus pull reader, every worker owns its own
periodic OTLP metric exporter. The Collector aggregates/exposes across
workers. The existing `create_prometheus_runtime` is still available for
single-process local setups and is unchanged.

The Collector's Prometheus exporter has no host-published port. Prometheus,
Tempo, Collector OTLP ingestion and Alertmanager also have no published
ports. Grafana is the only published service, bound to
`127.0.0.1:3000`. The shared telemetry network is Docker `internal: true`.
Alertmanager alone joins a second bridge with outbound access for webhook
delivery; its API remains unpublished.

## Install and secret prerequisites

Use Docker Engine with Compose v2 on the same host as the instrumented
application. Generate secrets **outside Git**. See the example file
`ops/observability/.env.example`.

Required inputs:

- `GRAFANA_ADMIN_PASSWORD_FILE`: an absolute, readable path containing a
  high-entropy Grafana admin password.
- `ALERT_WEBHOOK_URL_FILE`: an absolute, readable path containing a real
  **HTTPS** alert receiver endpoint, obtained from your incident platform.
  This stack deliberately contains no default webhook credential or
  silently discarded alert receiver.
- `GRAFANA_ADMIN_USER`: optional Grafana administrator name (default admin).

Create a local `ops/observability/.env` with these paths, **not** the
contents of the secrets. Root `.gitignore` ignores `.env`.
Do not place real secrets in CI logs, the repository, or the dashboard JSON.

### Launch and verify

```bash
# Relative to the repository root
docker compose --env-file ops/observability/.env \
  -f ops/observability/compose.yml config --quiet

docker compose --env-file ops/observability/.env \
  -f ops/observability/compose.yml up -d

docker compose --env-file ops/observability/.env \
  -f ops/observability/compose.yml ps
```

Visit **http://127.0.0.1:3000**, sign in with the configured Grafana
credentials, and open the *AI Interview Agent* folder. Grafana provisions
`uid: prometheus` and `uid: tempo`, and loads the dashboard
`ai-interview-api-ops` automatically. There are no automatic test metrics
until the API starts sending OTLP telemetry.

These Docker images use **fixed example tags**. Before a production release,
review current security advisories, pin image digest SHA256 values, configure
image signing/SBOM policies, and confirm volume permissions and platform
architecture. Docker volumes provide persistence, not off-host backups.

## Instrument the FastAPI service

Install optional SDK dependencies in the application image/environment:

```bash
uv pip install --python .venv/bin/python -r requirements-observability.txt
```

The **default** `src.api.app:app` is intentionally uninstrumented.
For the monitored entrypoint, explicitly configure and run:

```bash
# Application must share the Docker network with the Collector.
export INTERVIEW_OTLP_ENDPOINT='http://otel-collector:4318'
export INTERVIEW_ALLOW_LOCAL_OTLP_HTTP=true
uvicorn src.api.otel_app:build_otel_app --factory --host 0.0.0.0 --port 8000
```

Only use this HTTP endpoint on the isolated Docker network, never expose
OTLP ingress publicly. In a cross-host or Internet-facing deployment, use
an authenticated TLS/mTLS gateway and an `https://host:port` endpoint.
`create_otlp_runtime` rejects plain HTTP by default and only permits
explicit opt-in for localhost or the literal Docker service name
`otel-collector`. Arbitrary HTTP hosts, embedded credentials, URL paths,
and query strings are refused.

The existing `docker-compose.yml` for the API does not automatically join
the telemetry-private network or enable this opt-in entrypoint. Attach
the API service to the stack's private Docker network using a deployment
override or a deployment orchestrator, and set the three runtime settings
above. Changing the default application entrypoint is intentionally NOT
done in this PR to preserve its local workflow.

The factory creates an SDK runtime **per worker process**, installs ASGI
instrumentation without collecting bodies or raw URLs, and flushes/shuts
down SDK providers during the existing FastAPI lifespan teardown.
Network transport failures must not alter API responses.

For HTTPS remote OTLP with a private CA, inject the CA and credentials using
approved secret management, not a committed PEM or code constant. OTLP
headers may be injected through the runtime composition API; do not put
tokens into trace attributes.

## SLO alert policy

The example service-level objective is **99.9% HTTP availability** over a
rolling **30-day** period. Each HTTP `5xx` counts as a bad request; `2xx`,
`3xx` and `4xx` count as available. This is a business assumption to
review with the API owners (e.g., some 429s may be service failures).

Prometheus recording rules compute failure ratios over 5m, 30m, 1h, 6h
and 30d. Two multi-window alerts implement standard burn-rate guidance:

| Alert | Severity | Both windows | Error budget burn |
| --- | --- | --- | --- |
| InterviewAPIAvailabilityFastBurn | critical | 1h AND 5m | >14.4x |
| InterviewAPIAvailabilitySlowBurn | warning | 6h AND 30m | >6x |
| InterviewAPIExporterMissing | warning | no HTTP series 15m | no SLO data |

To reduce false positives, fast burn also requires >=100 requests in 1h
and >=10 in 5m; slow burn requires >=300 in 6h and >=30 in 30m. These
limits and the `for:` durations are defaults for **evaluation**, not a
site-specific paging policy. Prometheus retains 35 days locally to support
30-day ratio evaluation. Traffic below minimum thresholds will not trigger
burn-rate alerts; monitor low-volume services separately.

Alertmanager groups by alert name/severity, sends resolved notifications
to the configured webhook, and inhibits the *warning* variant if a
corresponding critical alert is active. This is a reference routing policy;
do not assume real incident paging works until the external webhook is
verified end-to-end.

The Grafana dashboard now uses a stable `prometheus` datasource UID (not
Grafana's manual-import `DS_PROMETHEUS` placeholder) so **file
provisioning actually resolves** its eight panels. The two new panels
show rolling 30-day 5xx ratio and 1-hour error-budget burn multiple.

## Validation and runbook

The new GitHub Actions `observability-stack` job validates:

1. Docker Compose syntax and network exposure constraints.
2. The Collector config using the real otelcol-contrib `validate` binary.
3. Prometheus config and recording/alert rules using real `promtool`.
4. Positive and no-traffic burn-rate scenarios using `promtool test rules`.
5. Alertmanager config using real `amtool`.
6. Grafana provisioning/datasource/dashboard JSON consistency.

The separate OTel SDK job uses a local HTTP capture server to prove
**real** OTLP metrics and traces are sent to distinct `/v1/metrics` and
`/v1/traces` endpoints; it does not rely only on mocks.

**Operator checks before release:** validate webhook delivery and retry,
enable TLS and authentication at external ingress, observe a live trace in
Tempo and a live histogram in Grafana, exercise a controlled error rate
alarm, restore named volumes from an off-host backup, and verify alert
silence/inhibition policies. Confirm worker fleet cardinality and scrape
sample volume with load tests.

**Known gaps:** Single-host failure domain, local Tempo storage, no
distributed storage/HA, no off-box audit or backups, no enforced RBAC for
monitoring tenants, no managed certificates, no automated SLO ownership or
incident escalation beyond the supplied webhook, no disaster recovery
exercise, and no organization-wide SLO compliance proof. Cross-host secure
OTLP ingress is *not* deployed by this Compose file.
