# Dataset Lineage — Phase 2, production-oriented foundation

This module records **dataset revision provenance**, separate from the
existing experiment lineage and the record-schema migration log. Each
revision is identified by `(dataset_id, semver)`, and its exact persisted
artifact bytes are represented by a SHA-256 digest. Raw samples are never
stored in the lineage repository.

## Components and SOLID boundaries

| Responsibility | Contract or component |
| --- | --- |
| Immutable provenance | `DatasetRevision`, `DatasetLineageNode`, `ParentLink` |
| Record-time policy | `DatasetLineageRecorder`, `validate_registration` |
| Ancestor/impact queries | `DatasetLineageExplorer` |
| Storage abstraction | `LineageWriter`, `LineageReader` protocols |
| SQLite persistence | `SQLiteDatasetLineageRepository` |
| Existing dataset bridge | `EvaluationDatasetLineageAdapter` |

Dependency flow: **application/domain -> ports <- infrastructure**.
The repository implements the same validation boundary as the recorder
so direct adapter use cannot circumvent graph policy. The existing
`DatasetVersion` remains the version of an aggregate, while
`schema_version` in lineage is optional **metadata**, not proof that an
external schema registry entry exists.

## Usage

```python
from datetime import UTC, datetime
from pathlib import Path

from src.evaluation.dataset.lineage import (
    DatasetLineageExplorer,
    DatasetLineageNode,
    DatasetLineageRecorder,
    DatasetRevision,
    LineageRelation,
    ParentLink,
)
from src.infrastructure.repositories.sqlite_dataset_lineage_repository import (
    SQLiteDatasetLineageRepository,
)

path = Path("data/lineage.sqlite")
path.parent.mkdir(parents=True, exist_ok=True)
store = SQLiteDatasetLineageRepository(path)
recorder = DatasetLineageRecorder(writer=store)

source = DatasetLineageNode.from_artifact(
    revision=DatasetRevision(dataset_id="interview-qa", version="1.0.0"),
    content=b"EXACT BYTES of the published source artifact",
    producer="ingest-v1",
    created_at=datetime.now(UTC),
)
recorder.register(node=source)

result = DatasetLineageNode.from_artifact(
    revision=DatasetRevision(dataset_id="interview-qa", version="1.1.0"),
    content=b"EXACT BYTES of the derived artifact",
    producer="normalize-v1",
    created_at=datetime.now(UTC),
)
registration = recorder.register(
    node=result,
    parents=(ParentLink(
        parent=source.revision,
        relation=LineageRelation.DERIVED_FROM,
    ),),
)
assert registration.created

ancestors = DatasetLineageExplorer(reader=store).ancestors(
    revision=result.revision
)
assert ancestors == (source.revision,)
```

Use `EvaluationDatasetLineageAdapter.build_node(dataset=...,
artifact_bytes=..., producer=...)` to connect an existing immutable
`EvaluationDataset` aggregate with the **bytes actually persisted**
by the caller. This avoids using incomplete projection hashes.
The application is responsible for publishing/storing the underlying
artifact, and verifying its digest at read time.

## Operational invariants

- One immutable content digest and provenance declaration per dataset
  identity/version. Conflicting re-registrations fail closed.
- Exact retries return the original event identifier without creating
  duplicate edges/audit rows, even if parent order differs.
- Parents must already exist; child and all its edges and audit event
  are committed in one `BEGIN IMMEDIATE` SQLite transaction.
- A new node is the only possible edge destination. Because parents
  already exist, this **append-only policy prevents cycles**. Same-dataset
  parent versions must be less than the child version.
- Multi-parent merges and cross-dataset derivations are supported.
- Ancestor and descendant queries are deterministic, cycle-defensive
  and bound by explicit `max_depth` and `max_nodes`. Overflows
  raise an error instead of returning an incomplete answer.
- Audit entries contain SHA-256, version, IDs, counts and timestamps.
  They intentionally omit raw record contents.
- Foreign keys and unique indexes are enabled. Concurrent write attempts
  serialize via SQLite's write lock; tests check same-event retries.

## Production readiness boundaries

This is a **production-oriented local provenance foundation**, not an
unqualified enterprise-wide governance system. In particular:

- Storage is file-backed SQLite. PostgreSQL migrations, replicated writes,
  backups, retention, and availability guarantees require deployment work.
- The SQLite file is not cryptographically tamper-evident. Administrators
  can modify or delete it; off-box signed audit anchoring is not implemented.
- No RBAC, tenant isolation, PII classification, access log, automated GDPR
  erasure policy, or organizational approval workflow is provided.
- The content digest proves only the bytes supplied by the caller. The
  module does not fetch remote artifacts or verify their hash on retrieval.
  Avoid including secrets in `producer` or dataset identifiers.
- The adapter does not atomically commit remote/object-storage artifacts
  together with SQLite lineage; use an outbox or orchestrated workflow for
  cross-system exactly-once behavior.
- Ancestor/impact queries make multiple reads, not a repeatable-read snapshot
  spanning other writers. A PostgreSQL graph-query adapter or a snapshot
  reader can supply stricter consistency for large graphs.
- This implementation does not perform complete source-data transformations
  or move the existing Schema Evolution migration snapshots.

## CI gates

```bash
uv run ruff check .
uv run pyright
uv run pytest -q
```

Behavioral tests cover immutable revision identity, multi-parent DAGs,
ordered traversal and bounded queries, missing-parent rollback, collision
rejection, fault-injected audit writes, concurrent retries, and restart
persistence.
