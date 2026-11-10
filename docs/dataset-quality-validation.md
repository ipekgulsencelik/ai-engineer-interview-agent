# Advanced Dataset Validation Engine — Phase 2

The engine evaluates serialized dataset sample records using composable,
testable rules. It deliberately separates **record rules** from **dataset-wide
rules** and returns a machine-readable, immutable `QualityReport`.

## Architecture (SOLID / Clean Architecture)

- `QualityIssue`, `QualityPolicy`, `QualityReport`: immutable domain values
- `RecordQualityRule` and `DatasetQualityRule`: small structural interfaces
- `RequiredFieldRule`, `NonEmptyStringRule`, `NumericRangeRule`,
  `AllowedValuesRule`, `UniqueFieldRule`: reusable, value-redacting rules
- `SchemaConformanceRule`: delegates to existing recursive
  `DatasetRecordValidator`, rather than duplicating the schema system
- `DatasetQualityEngine`: fail-closed orchestration, scoring and acceptance
- `QualityReportSerializer`: JSON-safe export, with no input records
- `DatasetQualityCoordinator`: evaluation followed by durable persistence
- `QualityReportStorePort`: small persistence protocol
- `SQLiteDatasetQualityReportRepository`: infrastructure adapter with
  immutable `run_id`, checksum verification, idempotency and bounded listing
- `EvaluationDatasetQualityAdapter`: reuses existing
  `EvaluationDatasetSerializer` and validates its serialized samples

Domain and application code do not import SQLite. New rules can implement the
small protocols without changing the engine.

## Example

```python
from pathlib import Path

from src.evaluation.dataset.quality import (
    DatasetQualityCoordinator,
    DatasetQualityEngine,
    NonEmptyStringRule,
    NumericRangeRule,
    QualityPolicy,
    RequiredFieldRule,
    UniqueFieldRule,
)
from src.infrastructure.repositories.sqlite_dataset_quality_report_repository import (
    SQLiteDatasetQualityReportRepository,
)

path = Path("data/dataset_quality.sqlite")
path.parent.mkdir(parents=True, exist_ok=True)
engine = DatasetQualityEngine(
    record_rules=(
        RequiredFieldRule(field_path="sample_id", rule_id="required-id"),
        NonEmptyStringRule(field_path="question", rule_id="question"),
        NumericRangeRule(
            field_path="score",
            minimum=0,
            maximum=1,
            rule_id="score-range",
        ),
    ),
    dataset_rules=(
        UniqueFieldRule(field_path="sample_id", rule_id="unique-id"),
    ),
    policy=QualityPolicy(min_pass_rate=0.98, max_errors=0, min_records=1),
)
coordinator = DatasetQualityCoordinator(
    evaluator=engine,
    store=SQLiteDatasetQualityReportRepository(path),
)

report = coordinator.evaluate_and_store(
    dataset_id="interview-samples",
    dataset_version="1.0.0",
    records=[
        {"sample_id": "a", "question": "What is RAG?", "score": 0.8},
        {"sample_id": "b", "question": "Define embedding", "score": 0.9},
    ],
)
assert report.accepted
assert report.total_checks == 7
```

## Scoring contract

- A **record check** = one record evaluated against one record rule.
- A **dataset check** = one complete dataset evaluated against one dataset rule.
- A check fails when its rule returns one or more issues. Multiple issues
  from the same check do **not** multiply the denominator.
- `pass_rate = passed_checks / total_checks` (between 0 and 1).
- Warnings count as failed checks, but `max_errors` gates only ERROR issues.
- `accepted` requires `record_count >= min_records`,
  `total_checks > 0`, `pass_rate >= min_pass_rate`, and
  `error_count <= max_errors`.
- **No checks** is never considered accepted, even if `min_records=0`.

This is a configured **quality-gate pass rate**, not a calibrated ML or
statistical "dataset quality score". Check portfolios must remain consistent
for comparisons across datasets. A single dataset-wide duplicate rule counts
as one failed check even if it reports multiple duplicate records; its
`error_count` and `failed_record_count` retain that additional detail.

## Safety and operational guarantees

- Rules are given deep copies, not references to the user's input records.
- Unexpected rule exceptions, invalid issue results, duplicate rule IDs and
  safety-limit overflow **fail closed**; they never produce an accepted report.
- Built-in rules do not echo sample field values in messages.
  **Custom rules must also avoid writing PII or secrets into issue messages.**
- Reports contain rule identifiers, codes, field paths, record indices and
  check counts, **not original records**. The SQLite adapter preserves both
  passing and failing reports with a checksum, and refuses changed content
  for the same `run_id`.
- SQLite writes use `BEGIN IMMEDIATE` with rollback on SQL failure.
  Concurrent identical saves create one row. Stored reports can be
  reloaded and queried with bounded `list_reports`.

## Explicit limits before organization-wide production

- Batch processing only: does not stream terabytes or shard distributed data.
- A finite `max_issues` guard exists; memory and CPU quotas are an
  **external** operational responsibility.
- No automatic PII detection, privacy classification or GDPR retention policy.
- No RBAC, tenant separation, encryption-at-rest management, signed audit
  anchoring, immutable off-box backups, alerts or distributed consistency.
- The report store uses file-backed SQLite, not a highly available database.
- Aggregates must already have valid `EvaluationDataset` entities; engine
  can validate raw serialized record mappings before aggregate construction.
- Built-in quality checks cover common constraints, not arbitrary cross-field
  business semantics. Domain-specific rules should be added via the protocols.
- A custom rule may be computationally expensive or malicious; implement
  resource limits, sandboxing or code review outside the engine as appropriate.

## CI

```bash
uv run ruff check .
uv run pyright
uv run pytest -q
```

Behavior tests exercise strict versus permissive gates, nested field paths,
duplicates, nonfinite values, schema conformance, extensions, fail-closed
behavior, input immutability, serialization, SQLite restart persistence,
duplicate saves, corruption detection and fault-injected transaction failure.
