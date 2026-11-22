# Required integration execution and skip policy

Normal developer test runs use `uv run pytest -q`. On Windows, **1567
passed and 43 skipped** were reported (2026-11-22). Many of those skips
are deliberate when a disposable PostgreSQL instance or optional
OpenTelemetry/Prometheus packages are not installed. Skipped tests are
not equivalent to passed tests.

The repository already has two independent, green **real integration**
CI jobs at [run 45062645695](https://github.com/ipekgulsencelik/ai-engineer-interview-agent/actions/runs/45062645695):

- PostgreSQL + Alembic: **16 passed**, with a disposable PostgreSQL 16
  service and `POSTGRES_TEST_DSN` set only in the integration job.
- OpenTelemetry SDK + Prometheus: **40 passed**, using the optional
  dependencies in `requirements-observability.txt`.

No local database connection string or secret is required for running
the general Python suite. **Do not set `POSTGRES_TEST_DSN` to any real
or shared production database**: the PostgreSQL integration tests
truncate tables and create/drop roles.

## New fail-closed policy

Each required live integration CI job now emits JUnit XML. An
independent standard-library-only evaluator verifies that the report
exists, has consistent counts, includes at least one testcase, and has
**zero skipped, failed or errored testcases**. The validation still
runs when pytest fails or does not create a report. Exact JUnit evidence
is archived for 14 days; the job cannot become green just because
`pytest.importorskip` silently skipped all required tests.

General CI now uses `uv run pytest -q -rs` so skip reasons are visible
for classification. This **does not** turn expected local skips into
failures or weaken the existing release/Docker vulnerability checks.
The required real integration CI jobs, not an unconfigured Windows
installation, are the acceptance environments for database and SDK
behavior.

For independent local verification, run `uv run pytest -q -rs` and
consult the skip summary. Install optional dependencies only in an
isolated development environment. PostgreSQL integration tests require
a disposable test instance, schema migrations and explicit approved
test credentials.
