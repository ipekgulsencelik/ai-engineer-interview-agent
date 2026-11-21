# PostgreSQL Monitoring: tenant RLS and database RBAC

## Scope and trust boundary

This increment adds **database-enforced tenant isolation** to the four
existing PostgreSQL monitoring tables:

- `dataset_monitor_snapshots`
- `dataset_monitor_alert_outbox`
- `dataset_monitor_alert_receipts`
- `dataset_monitor_alert_delivery_events`

It does **not** apply to every dataset/report table, FastAPI endpoint,
Streamlit page, SQLite repository, Grafana instance, or organization-wide
identity provider. Do not claim full application multi-tenancy from this PR.

Migration `20261121_03` applies both `ENABLE ROW LEVEL SECURITY` and
`FORCE ROW LEVEL SECURITY` to all four tables. Every row has a validated
`tenant_id`, and composite foreign keys prevent attaching an alert,
delivery receipt, or audit event to another tenant's parent.

### Why NOT `SET app.tenant_id`

Arbitrary PostgreSQL custom session settings can be changed by any user who
can execute SQL, so **they are not a trusted authorization boundary**.

Instead, tenant identity is derived by
`monitoring_security.current_tenant()`, a carefully scoped,
`SECURITY DEFINER` function using **`SESSION_USER`**, backed by
`monitoring_security.tenant_login_bindings`. Application roles cannot
read or change this mapping. An unregistered login resolves to `NULL`
and is denied by RLS.

Each tenant therefore needs its own **managed PostgreSQL LOGIN role**
(or a separate login per tenant and action). Application connection pools
must be keyed by this trusted login. Sharing one PostgreSQL login across
different tenants destroys this isolation model. `SET ROLE` does not
change `SESSION_USER` and cannot switch tenant identity.

**PostgreSQL superusers and roles with `BYPASSRLS` can still bypass RLS.**
Migration/service-owner credentials MUST NOT be used by API requests,
tenant services or background workers. The database login must also NOT
own these monitoring tables or have DDL/CREATEROLE privileges.

## Rollout order

1. Stop monitoring writers and alert dispatchers. Take a backup and verify
   a restore to a separate PostgreSQL database. Review legacy records and
   the tenant ownership mapping **before** migration.
2. With a **separate trusted migration account**, run:
   `python -m alembic -c db/postgres/alembic.ini upgrade head`.
   This backfills the existing rows to `tenant_id='legacy'`. Existing
   legacy records are NOT automatically assigned to a real tenant.
3. With a **DBA account**, run `db/postgres/tenant_roles.sql` once
   (idempotent). It creates **NOLOGIN** group roles
   `interview_monitor_reader`, `interview_monitor_writer`, and
   `interview_monitor_dispatcher`, with distinct SQL privileges.
4. Create **individual LOGIN roles** with unique secrets, one per
   tenant/permission boundary, and grant the appropriate group role:
   `GRANT interview_monitor_writer TO tenant_acme_writer;`
5. Insert DBA-controlled bindings, for example:
   `INSERT INTO monitoring_security.tenant_login_bindings
   (login_role, tenant_id) VALUES ('tenant_acme_writer', 'acme');`
   Only the DBA/migration role may manage bindings. Map *legacy*
   records intentionally with a separately approved, audited migration;
   do not make them accessible to every tenant.
6. Connect each API/worker using its managed role's credentials via the
   existing `PsycopgConnectionFactory`. Do not use the DBA DSN or expose
   role credentials to clients. In production the factory defaults to
   `sslmode=verify-full`.
7. Run real cross-tenant access tests in staging before enabling traffic.
   Do not deploy a rollback (which drops tenant columns and RLS) to a live
   multi-tenant database without a data recovery and incident plan.

## Role matrix (SQL-layer)

| SQL role | SELECT | INSERT | UPDATE |
| --- | --- | --- | --- |
| `interview_monitor_reader` | 4 monitoring tables | none | none |
| `interview_monitor_writer` | inherited reader | snapshots, outbox | none |
| `interview_monitor_dispatcher` | inherited reader | receipts, audit events | alert outbox |

Only DBA accounts can insert/update the role-to-tenant mapping. Tenant
roles are neither superuser, table owner, CREATEROLE, nor BYPASSRLS.
No tenant service should have `TRUNCATE` or `DELETE` permissions.

SQL row privileges are intentionally **coarse** for alert lifecycle
operations: the dispatcher can alter lease state and, at the SQL layer,
also change a dead-letter flag. Action-level authorization for operator
requeue is **not** enforced by these grants. An authenticated operator
API / stored procedure layer with independent requeue permission is
required before exposing that operation externally. No tenant credentials
are issued or managed automatically by the Python application.

## Data integrity and limitations

- Existing globally unique `monitor_run_id` and `alert_id` constraints
  are unchanged. Two tenants cannot reuse a global ID; use generated UUIDs.
- RLS returns no rows for another tenant's snapshot, outbox, receipt or
  audit record. Child rows additionally require matching
  `(parent_id, tenant_id)` **composite foreign keys**.
- Existing application monitoring repositories and leased dispatcher
  require **no tenant_id user parameter**: the database fills it from the
  authenticated tenant login and revalidates on every SQL operation.
- Tests use disposable PostgreSQL LOGIN roles against a real PostgreSQL 16
  service; check both unauthorized and permitted actions.
- RLS is defense in depth, not a replacement for authentication, endpoint
  authorization, mTLS, credential rotation, audit retention, rate limiting,
  or external security review.
- Isolation does not protect against privileged DBA access, secrets
  compromise, SQL that runs as a more privileged role, shared database
  login reuse, malicious extensions or misconfigured connection pooling.
- Database RLS does not yet isolate Prometheus/Grafana or Tempo data
  streams. Separate observability tenants / auth are required there.
- No HA/failover, PITR or disaster recovery has been built in this PR.
  Those require an independently tested deployment and backup runbook.

## CI commands

Default gates:

```bash
uv run ruff check .
uv run pyright
uv run pytest -q
```

PostgreSQL test job (disposable postgres:16-alpine service):

```bash
python -m alembic -c db/postgres/alembic.ini upgrade head

python -m pytest -q \
  tests/infrastructure/repositories/test_postgres_monitoring_integration.py \
  tests/infrastructure/repositories/test_postgres_tenant_security.py
```

Tests include migration head, non-superuser readers/writers/dispatchers,
tenant A/B isolation, unbound-login denial, GUC spoof resistance,
unauthorized direct updates and cross-tenant parent FK rejection.
