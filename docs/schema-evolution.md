# Schema Evolution — Production Hardening (Phase 2)

Versioned dataset record schemas are separate from dataset content versions.
This package does **not** mutate immutable `EvaluationDataset` domain aggregates.

## Architecture and SOLID

- `DatasetField`, `DatasetRecordSchema`: immutable schema value objects
- `DatasetRecordValidator`: recursive record validation, no implicit coercion
- `SchemaCompatibilityChecker`: breaking/safe changes, including nested fields
- `MigrationRegistry`: forward-only, unambiguous version paths
- `SchemaEvolutionService`: migration orchestration and step validation
- `DatasetMigrationCoordinator`: validates before durable commit
- `SQLiteDatasetSchemaRepository`: persistent immutable schema definitions
- `SQLiteDatasetMigrationStore`: transactional snapshots and durable audit
- `LoggingDatasetMigrationTelemetry`: best-effort metadata-only logging

The core components depend on structural Python `Protocol` interfaces,
not SQLite or a particular logger. Infrastructure adapters are isolated
under `src/infrastructure`.

## Validated nested types

`DatasetField` supports `properties=(...)` on objects and `items=...`
on arrays. Unknown fields, invalid nested types, missing required fields,
non-finite numbers and non-nullable nulls are rejected. Primitive types are
`string`, `integer`, `number`, `boolean`, `object` and `array`.
Unconstrained objects/arrays remain supported for backwards compatibility.
This is **not** yet full JSON Schema (e.g., regex, unions, deep cross-field
constraints and recursion depth limits are not provided).

Compatibility reports ask whether **old valid records** can be read by the
**new strict validator**. Removing an old field is breaking because old
records would now contain unexpected keys; removing nested constraints is
compatible. Reported compatibility does not auto-migrate records.

## Persistent and audited migration example

```python
from pathlib import Path

from src.evaluation.dataset.schema_evolution import (
    DatasetField,
    DatasetRecordSchema,
    DatasetMigrationCoordinator,
    MigrationRegistry,
    MigrationStep,
    RenameField,
    SchemaEvolutionService,
)
from src.infrastructure.logging.dataset_migration_telemetry import (
    LoggingDatasetMigrationTelemetry,
)
from src.infrastructure.repositories.sqlite_dataset_schema_repository import (
    SQLiteDatasetSchemaRepository,
)
from src.infrastructure.repositories.sqlite_dataset_migration_store import (
    SQLiteDatasetMigrationStore,
)

db_path = Path("data/schema_evolution.sqlite")
db_path.parent.mkdir(parents=True, exist_ok=True)

registry = SQLiteDatasetSchemaRepository(db_path)
store = SQLiteDatasetMigrationStore(db_path)

old = DatasetRecordSchema(
    name="interview_samples",
    version="1.0.0",
    fields=(DatasetField("answer", "string"),),
)
new = DatasetRecordSchema(
    name="interview_samples",
    version="2.0.0",
    fields=(DatasetField("candidate_answer", "string"),),
)
registry.register(schema=old)
registry.register(schema=new)

migrations = MigrationRegistry([
    MigrationStep(
        from_version="1.0.0",
        to_version="2.0.0",
        operations=(RenameField("answer", "candidate_answer"),),
    )
])
coordinator = DatasetMigrationCoordinator(
    migrator=SchemaEvolutionService(
        migrations=migrations,
        intermediate_schemas=registry,
    ),
    persistence=store,
    telemetry=LoggingDatasetMigrationTelemetry(),
)
event = coordinator.execute(
    records=[{"answer": "Retrieval plus generation"}],
    source_schema=old,
    target_schema=new,
)
assert event.operation == "migration"
assert store.current_snapshot(schema_name=old.name).schema_version == "2.0.0"

# Explicit rollback moves the active snapshot back to the source version.
rollback = coordinator.rollback_last(schema_name=old.name)
assert rollback.operation == "rollback"
```

## Transactional guarantees and limits

A local SQLite `BEGIN IMMEDIATE` transaction atomically writes new snapshots,
moves the active pointer, and appends a migration audit event. A failed SQL
statement rolls back those writes; a failed migration validation never writes
anything. Concurrent/stale requests are rejected by the expected source
version **and content checksum**. Stored snapshots permit explicit rollback
of the latest committed migration, with a separate audit event. Audit events
include versions, hashes, record counts, and timestamps, **not raw answers**.
Audit event metadata and raw snapshots are stored in the same SQLite file;
protect that file according to your data privacy needs.

SQLite snapshot rollback does **not** roll back external database writes,
remote APIs, object storage or side effects of custom migration operations.
Custom `MigrationOperation` implementations should be deterministic and
side-effect free. This implementation is a durable local transaction boundary,
not distributed two-phase commit, nor an externally replayable workflow.

For multi-hop migrations, pass `intermediate_schemas=registry` to
`SchemaEvolutionService` so each intermediate version is validated.
The optional parameter remains absent by default to preserve compatibility
with older in-memory use cases, so production composition must pass it.

The system does not yet persist failed validation attempts, enforce cross-
process authorization, offer nested JSON Schema `$ref`, perform external
storage migration, provide automatic disaster recovery/backups, or support a
distributed database. Those are separate production deployment concerns.

## Quality gates

```bash
uv run ruff check .
uv run pyright
uv run pytest -q
```

Integration tests cover schema round-trip, nested validation, multi-hop
migration, stale-source detection, audit persistence, explicit rollback,
transaction failure injection, and telemetry failures.
