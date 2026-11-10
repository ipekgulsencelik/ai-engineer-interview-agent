# PostgreSQL + Alembic: monitoring persistence foundation

The existing production-oriented SQLite monitoring adapters remain available.
PostgreSQL is an **opt-in** infrastructure implementation of the same narrow
application ports, not a replacement for dataset quality, lineage, or schema
migration logic.

## Components / architectural boundaries

- `PostgresDatasetObservabilityRepository` implements `MonitoringWriter`
  and `MonitoringReader` with transactional snapshot + outbox creation.
- `PostgresLeasedDatasetAlertOutbox` implements `LeasedAlertOutbox`, with
  `SELECT ... FOR UPDATE SKIP LOCKED` for concurrent claims, token fencing,
  exponential retries, durable delivery receipts, and dead-letter requeue.
- `PsycopgConnectionFactory` is an infrastructure-only driver boundary.
  It defaults to `sslmode=verify-full` and a bounded connection timeout.
- `db/postgres/versions` contains Alembic-managed schema changes:
  `20261110_01` (monitor snapshots, outbox and receipts) and
  `20261110_02` (leased delivery and audit events).
- Domain/application contracts, alert serializer and the
  `LeasedDatasetAlertDispatcher` are unchanged.

Database tables are *not* auto-created when adapters are instantiated.
**Alembic must be run as a separate, authorized deployment step.**

## Local deployment and migration

Use a dedicated PostgreSQL 16+ database with least-privilege accounts.
Prefer separate migration and application roles. The app role should not
be allowed to change schema or drop tables.

```bash
uv pip install --python .venv/bin/python -r requirements-postgres.txt

# Alembic uses SQLAlchemy's psycopg URL, supplied via environment:
export POSTGRES_DATABASE_URL='postgresql+psycopg://user:password@db.example.com/monitoring?sslmode=verify-full'
uv run --no-sync python -m alembic -c db/postgres/alembic.ini upgrade head

# Application driver uses psycopg's native URL (without +psycopg):
export POSTGRES_DSN='postgresql://user:password@db.example.com/monitoring?sslmode=verify-full'
```

On Windows PowerShell, use `$env:POSTGRES_DATABASE_URL = '...'` instead
of `export`. Never commit DSNs, passwords, TLS keys or connection strings.
Use a secret manager in production. The test workflow uses **disposable**
local credentials against a GitHub Actions PostgreSQL service.

Example composition:

```python
import os

from src.evaluation.dataset.observability import (
    DatasetObservabilityCoordinator,
    DatasetObservabilityMonitor,
    LeasedDatasetAlertDispatcher,
)
from src.infrastructure.logging.dataset_monitoring_alert_sender import (
    LoggingMonitoringAlertSender,
)
from src.infrastructure.repositories.postgres_connection import (
    PsycopgConnectionFactory,
)
from src.infrastructure.repositories.postgres_dataset_observability_repository import (
    PostgresDatasetObservabilityRepository,
)
from src.infrastructure.repositories.postgres_leased_dataset_alert_outbox import (
    PostgresLeasedDatasetAlertOutbox,
)

connect = PsycopgConnectionFactory(dsn=os.environ["POSTGRES_DSN"])
monitor_store = PostgresDatasetObservabilityRepository(connect=connect)
outbox = PostgresLeasedDatasetAlertOutbox(connect=connect)

coordinator = DatasetObservabilityCoordinator(
    monitor=DatasetObservabilityMonitor(), store=monitor_store
)
dispatcher = LeasedDatasetAlertDispatcher(
    outbox=outbox,
    sender=LoggingMonitoringAlertSender(),
    worker_id="monitor-worker-1",
    lease_seconds=60,
)
```

Use the existing coordinator to save monitoring snapshots and call
`dispatcher.dispatch_once(limit=...)` under your deployment's supervisor.

## Data correctness and delivery guarantees

- Monitoring snapshot and initial alert outbox inserts commit in **one**
  PostgreSQL transaction, protected by a unique monitor-run identity.
- Conflicting replay fails closed; exact replay is idempotent.
- Multiple PostgreSQL workers claim disjoint **unexpired** alerts via row
  locks and `SKIP LOCKED`. Ownership is fenced by token, worker, attempt,
  and expiry on acknowledgment/failure writes.
- Expired claims are recovered in bounded batches of up to 1,000; retries
  use exponential backoff and terminal failures enter the Dead-Letter Queue.
- Claim, retry, dead-letter, requeue and receipt state changes are
  transactional with metadata-only delivery audit events ordered by\n  a database-generated sequence number.
- Requeue must be protected by an external **authorized operator**
  workflow. The data layer alone is not an authorization boundary.
- Delivery remains **at-least-once**. A send that succeeds before a worker
  crash can be repeated when the claim expires; external notification
  providers should deduplicate on stable `alert_id`.
- An alert must not be sent under a lease shorter than the maximum expected
  time of the *full batch*. Token fencing prevents stale acknowledgments,
  not duplicate sends that already reached an external provider.
- Compared with SQLite, PostgreSQL supports per-row lock concurrency.
  Connection pooling, query load and index behavior require production
  benchmarking; this PR does not claim measured SLAs.

## Deployment safety / limitations

- Alembic migrations should run before app rollout, against a backup and
  tested restore procedure. Downgrades remove tables/columns and may destroy
  monitoring history; do not downgrade production data without an approved
  recovery plan.
- Use a distinct schema/database for these monitoring tables. Existing
  SQLite files are **not** automatically copied to PostgreSQL. Data
  migration/backfill is separate work.
- PostgreSQL dependencies are explicitly in
  `requirements-postgres.txt`, not in the core `uv.lock`. Release
  engineering should compile a fully pinned, hash-verified deployment
  environment before deployment.
- TLS `verify-full` is enabled by default in the connection factory.
  The integration test disables it only for localhost CI.
- Exception messages from the driver are not emitted by the adapters,
  since a DSN could contain sensitive information.
- No multi-tenant RLS, RBAC, encrypted backups, off-box signed audit,
  OpenTelemetry traces, Prometheus service metrics or scheduler are
  included in this increment.
- PostgreSQL integration tests use a real disposable PostgreSQL 16 service
  in GitHub Actions; no external database is required for the default
  unit-test job.

## CI validation

```bash
uv run ruff check .
uv run pyright
uv run pytest -q

# Dedicated CI job:
# PostgreSQL 16 service -> alembic upgrade head -> PostgreSQL integration tests
```

The integration suite checks Alembic head, transactional snapshot writes,
idempotency, conflict detection, SKIP LOCKED concurrency, expiry fencing,
retry/dead-letter handling and failed receipt rollback. Additional
staging and load testing is still required for a production launch.
