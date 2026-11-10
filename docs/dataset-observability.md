# Dataset Observability & Data Quality Monitoring — Phase 2

A **production-oriented local foundation** for data quality monitoring,
distribution drift, durable monitoring snapshots, and delivery-retryable
alert events. This module **reuses** the existing
`DatasetDriftAnalyzer`, `DatasetDistributionSnapshot` and `QualityReport`
rather than introducing a parallel scoring/quality system.

## Architecture / SOLID

| Concern | Implementation |
| --- | --- |
| Invariants & policy | `MonitoringPolicy`, `MonitoringSnapshot`, `MonitoringAlert` |
| Monitoring logic | `DatasetObservabilityMonitor` |
| Drift calculation | Injected `DriftAnalyzerPort`; existing `DatasetDriftAnalyzer` default |
| Application orchestration | `DatasetObservabilityCoordinator` |
| Durable writes / reads | `MonitoringWriter`, `MonitoringReader` protocols |
| Alert transport | `AlertOutbox`, `AlertSender` protocols |
| Dispatch and retries | `DatasetAlertDispatcher` |
| SQL adapter | `SQLiteDatasetObservabilityRepository` (infrastructure layer) |
| Safe example sender | `LoggingMonitoringAlertSender` (infrastructure layer) |

Domain and application code never depend on SQLite or external messaging
frameworks. To use email, Slack or a pager, implement `AlertSender`. To
use PostgreSQL, implement `MonitoringWriter`, `MonitoringReader`, and
`AlertOutbox` with the same transactional semantics.

## Monitoring metrics and alarm thresholds

`DatasetDriftAnalyzer` calculates the **largest absolute change in
category/level/split bucket proportions**. This is a bounded [0,1]
heuristic, **not** population stability index, statistical hypothesis test
or model prediction drift.

`pass_rate_drop = max(0, baseline_quality.pass_rate -
comparison_quality.pass_rate)`. This metric compares **quality check pass
rates**; if the underlying rule portfolios differ, the comparison is not
statistically meaningful.

The monitor produces deterministic signal codes:

- `QUALITY_GATE_REJECTED`: critical if comparison `QualityReport.accepted`
  is false.
- `INSUFFICIENT_SAMPLES`: critical if comparison record count is below
  `min_comparison_records`.
- `DRIFT_WARNING` or `DRIFT_CRITICAL`: based on configured severity bands.
- `QUALITY_REGRESSION_WARNING` or `QUALITY_REGRESSION_CRITICAL`:
  based on configured quality pass-rate drop bands.

Thresholds are **inclusive** (`observed >= threshold`), with critical
conditions taking precedence over warnings for each metric. The overall
status is `healthy`, `warning`, or `critical` based on the most severe
signal. The original threshold policy is embedded in every snapshot.

The monitor **fails closed** when baseline and comparison report
identities/counts are mismatched, or when an input distribution sums to a
different record count. Empty checked datasets are rejected, because the
underlying drift calculator otherwise reports zero when a distribution
total is zero. Baseline report timestamps cannot be later than comparison.

## Example: evaluate, save, dispatch

```python
from pathlib import Path

from src.evaluation.dataset.observability import (
    DatasetAlertDispatcher,
    DatasetObservabilityCoordinator,
    DatasetObservabilityMonitor,
    MonitoringPolicy,
)
from src.infrastructure.logging.dataset_monitoring_alert_sender import (
    LoggingMonitoringAlertSender,
)
from src.infrastructure.repositories.sqlite_dataset_observability_repository import (
    SQLiteDatasetObservabilityRepository,
)

store_path = Path("data/monitoring.sqlite")
store_path.parent.mkdir(parents=True, exist_ok=True)
store = SQLiteDatasetObservabilityRepository(store_path)

coordinator = DatasetObservabilityCoordinator(
    monitor=DatasetObservabilityMonitor(
        policy=MonitoringPolicy(
            drift_warning=0.1,
            drift_critical=0.25,
            pass_rate_drop_warning=0.05,
            pass_rate_drop_critical=0.15,
        )
    ),
    store=store,
)

# These are real values produced by existing analyzers/quality evaluation.
snapshot = coordinator.evaluate_and_store(
    baseline_distribution=baseline_distribution,
    comparison_distribution=comparison_distribution,
    baseline_quality=baseline_quality_report,
    comparison_quality=comparison_quality_report,
)

# Schedule this separately; the module does not run background jobs.
dispatcher = DatasetAlertDispatcher(
    outbox=store,
    sender=LoggingMonitoringAlertSender(),
)
delivered_count = dispatcher.dispatch_pending(limit=100)
```

`LoggingMonitoringAlertSender` writes structured metadata-only logs.
It is **not an external paging, ticketing or email integration**.

## Durability, idempotency and delivery semantics

- Snapshot and new pending alert rows are stored in **one SQLite
  `BEGIN IMMEDIATE` transaction** with foreign keys.
- `monitor_run_id` is immutable: exact replay returns `False`, while
  conflicting content fails closed. SHA-256 verifies stored bytes against
  accidental corruption (not hostile tampering).
- Run history is read via bounded `list_snapshots` and pending alerts via
  bounded `pending`; both are stable across process restarts.
- A sender failure leaves the alert pending. Successful delivery gets a
  durable, transactional receipt and removes the event from pending results.
- **At-least-once** delivery: a process crash between external send and
  SQLite receipt may duplicate an alert. External senders should deduplicate
  by stable `alert_id`.
- Multi-process concurrent dispatch is **not** leased/claimed: two workers
  can send the same pending alert concurrently. Use a single dispatcher
  worker per SQLite file or implement leasing in a future adapter.
- No raw sample content is stored in the snapshot/outbox payloads.
  Dataset IDs and alert identifiers are metadata: do not put secrets there.

## Explicit enterprise gaps

This is a **foundation**, not a fully deployed enterprise monitoring stack.
Additional work is needed for PostgreSQL HA, tenant isolation, RBAC, managed
encryption, immutable signed off-box audit, retention/GDPR policies,
OpenTelemetry/Prometheus integration, dashboard/query APIs, supervised
scheduler, alert routing and escalation, distributed outbox leasing,
production backup/recovery tests, and cross-store transactions with the
quality report repository.

Quality reports and distribution snapshots are supplied by the caller; this
module does not schedule regular evaluations, discover new datasets, or
verify that all compared quality reports used identical rule sets.

## CI

```bash
uv run ruff check .
uv run pyright
uv run pytest -q
```

Unit/integration tests cover healthy, warning, critical, empty/mismatched
input, threshold policies, round-trip serialization, restart persistence,
concurrent idempotent saves, transaction fault injection, failed delivery,
acknowledgment rollback, duplicate receipts and checksum validation.
