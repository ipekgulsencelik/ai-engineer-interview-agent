# Dataset alert delivery: leased workers, retries and dead-letter operations

This module hardens the monitoring alert outbox created in PR #27.

## Architecture and SOLID boundaries

The existing monitoring models, snapshots, and outbox tables remain intact.
New application contracts live under
`src.evaluation.dataset.observability.delivery`:

- `AlertLease`, `AlertFailureOutcome`, `AlertDispatchSummary`:
  immutable delivery/claim values.
- `AlertRetryPolicy`: bounded exponential retry/backoff policy.
- `LeasedAlertOutbox`: small storage port for claim, fenced acknowledge,
  failure transitions, dead-letter inspection, and operator requeue.
- `LeasedDatasetAlertDispatcher`: application orchestration, depending only
  on `LeasedAlertOutbox` and the existing `AlertSender` protocol.
- `SQLiteLeasedDatasetAlertOutbox`: transactional infrastructure adapter,
  isolated under `src/infrastructure/repositories`.
- `DeliveryClock`: injectable UTC clock for deterministic time tests.

Transport is **outside** SQL transactions. Existing
`SQLiteDatasetObservabilityRepository.save` continues to atomically create
the monitoring snapshot and initial outbox alerts. The new adapter adds
delivery-specific columns and audit events without rewriting past snapshots.

## Operational semantics

1. A worker atomically **claims** eligible alerts with `BEGIN IMMEDIATE`.
   The claim supplies a random per-attempt fencing token and expiry, and
   increments the durable attempt counter.
2. Only the current worker/token/attempt before expiry can **acknowledge**
   or **fail** a claim. A stale worker cannot acknowledge a later worker's
   claim.
3. Failures are recorded with a fixed uppercase **reason code**, without raw
   exception text. Retry eligibility is delayed using exponential backoff
   capped by `max_delay_seconds`.
4. A crash leaves a lease outstanding until expiry; the next claim call
   recovers it, either scheduling a retry or dead-lettering an exhausted
   attempt.
5. At `max_attempts`, terminal failures enter the **dead-letter** queue.
   They do not silently disappear. An operator may explicitly requeue
   an alert, which resets attempts and writes an auditable `requeued`
   event.
6. Successful sending creates a durable delivery receipt and an append-only
   `delivered` event **in the same transaction**.

The adapter keeps metadata-only audit event entries for claimed, retry,
lease-expired, delivered, dead-lettered and requeued transitions. Transactions
make the state change and corresponding event atomic, and SQL fault injection
tests verify rollback behavior.

## Example

```python
from pathlib import Path

from src.evaluation.dataset.observability.delivery import (
    AlertRetryPolicy,
    LeasedDatasetAlertDispatcher,
)
from src.infrastructure.logging.dataset_monitoring_alert_sender import (
    LoggingMonitoringAlertSender,
)
from src.infrastructure.repositories.sqlite_leased_dataset_alert_outbox import (
    SQLiteLeasedDatasetAlertOutbox,
)

path = Path("data/monitoring.sqlite")
outbox = SQLiteLeasedDatasetAlertOutbox(
    path,
    policy=AlertRetryPolicy(
        max_attempts=5,
        initial_delay_seconds=10,
        max_delay_seconds=3600,
    ),
)
dispatcher = LeasedDatasetAlertDispatcher(
    outbox=outbox,
    sender=LoggingMonitoringAlertSender(),
    worker_id="worker-1",  # unique and stable per running worker
    lease_seconds=60,
)

result = dispatcher.dispatch_once(limit=10)
print(result.delivered, result.retry_scheduled, result.dead_lettered)

# Operational intervention requires authorization at the application boundary:
for alert in outbox.dead_letters(limit=100):
    print(alert.alert_id, alert.code)
    # outbox.requeue(alert_id=alert.alert_id)  # ONLY after operator review
```

`LoggingMonitoringAlertSender` only writes to the local log system. It is
not a Slack, email, or incident paging integration.

## Backward compatibility and migration

- Instantiate the **new** leased adapter against the existing file-backed
  monitoring SQLite database to perform its idempotent in-place schema
  upgrade. The old monitoring `save`, `get` and `list_snapshots`
  operations continue to work.
- After upgrade, the old `pending` / `mark_delivered` direct-dispatch
  API rejects calls **fail closed**. This is intentional: otherwise legacy
  workers could bypass leases and cause duplicate delivery.
- Before rollout, stop legacy dispatchers, create a SQLite backup, and
  roll out new workers against the upgraded database. The schema migration
  is forward-only; there is no automated downgrade.
- Use the **same** retry policy across all worker instances. Attempts are
  stored durably; policies are process configuration, not per-alert policy.
- The repository must be located on storage with reliable SQLite file
  locking. Network filesystems with unreliable locks are not supported.
- Choose `lease_seconds` safely longer than the expected time to send **all
  alerts claimed in a batch**. An operation exceeding its lease can be
  externally delivered but cannot be acknowledged; subsequent attempts
  may resend. Set small batch limits or implement heartbeat renewal in a
  follow-up if delivery latency is unpredictable.

## Guarantees and enterprise gaps

**Guaranteed by this implementation (subject to SQLite assumptions):**
- Concurrent workers cannot hold the **same unexpired lease** simultaneously.
- A stale lease token cannot acknowledge after an expiry/reclaim.
- Database writes, audit events, and delivery receipts are transactional.
- Explicit, bounded exponential retry and operator-visible terminal failures.
- Existing monitoring snapshots remain immutable and value-only.

**Not guaranteed:**
- Exactly-once external delivery. If a worker sends but crashes before
  acknowledging, delivery can be duplicated. Integrations MUST deduplicate
  with stable `alert_id`.
- Long-lived task lease renewal and cross-system transaction coordination.
- A supervisor or scheduler to invoke `dispatch_once`; scheduling is
  external. The logging sender alone does not page incident responders.
- Organization-wide authorization/RBAC and tenant isolation for requeue.
- Highly available PostgreSQL storage, managed backups, encryption, disaster
  recovery, OpenTelemetry exporters, distributed traces or alert escalation.
- Tamper-proof off-box signed delivery audit logs.
- Production-scale stress/load tests and fault testing with real paging APIs.

This is an incremental **production-oriented** improvement; it does not
establish whole-system Enterprise-Level compliance or availability SLAs.

## Quality gates

```bash
uv run ruff check .
uv run pyright
uv run pytest -q
```

Tests cover concurrent claims, lease expiry, ownership fencing, retry/backoff
schedules, dead-letter and operator requeue flows, fault-injected claim and
acknowledgment writes, SQLite restart durability, old API fail-closed behavior,
and no leaked exception payloads in durable records.
