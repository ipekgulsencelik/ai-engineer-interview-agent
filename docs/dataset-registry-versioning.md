# Phase 2 — Dataset Registry & Versioning Foundation

This increment adds a content-addressed, **immutable** dataset catalog
without duplicating the existing Dataset Lineage or Schema Evolution models.

## Clean Architecture boundaries

- Domain model: `DatasetCatalogEntry` and `CatalogRegistration`
- Narrow ports: `DatasetLineageLookup`, `RegistryReader`, `RegistryWriter`
- Application: `DatasetRegistryService` checks registered lineage equality
- Infrastructure: `SQLiteDatasetRegistryRepository`
- Integration: reuse `DatasetRevision`, `DatasetLineageNode` and strict
  `parse_schema_version` from existing Phase 2 packages

The repository stores **metadata only**: dataset identity, semantic version,
SHA-256 of the exact artifact bytes supplied when building the lineage node,
producer, created_at, display name, owner identifier, optional schema version,
canonical lowercase tags, and a short description. **It never stores raw
interview answers, evaluation samples, CVs, artifact bytes or prompt content.**

A SHA-256 digest authenticates the bytes supplied by the caller only; this
local catalog does not fetch artifacts from remote storage or independently
verify them. An optional `schema_version` records provenance metadata and
does not attest that a schema registry entry exists.

## Publish a lineage-backed dataset

```python
from datetime import UTC, datetime
from pathlib import Path

from src.evaluation.dataset.lineage import (
    DatasetLineageNode,
    DatasetLineageRecorder,
    DatasetRevision,
)
from src.evaluation.dataset.registry import DatasetRegistryService
from src.infrastructure.repositories.sqlite_dataset_lineage_repository import (
    SQLiteDatasetLineageRepository,
)
from src.infrastructure.repositories.sqlite_dataset_registry_repository import (
    SQLiteDatasetRegistryRepository,
)

lineage = SQLiteDatasetLineageRepository(Path("data/lineage.sqlite"))
registry = SQLiteDatasetRegistryRepository(Path("data/registry.sqlite"))

node = DatasetLineageNode.from_artifact(
    revision=DatasetRevision(dataset_id="interview-qa", version="1.0.0"),
    content=b"EXACT BYTES published to an independent artifact store",
    producer="evaluation-pipeline",
    created_at=datetime.now(UTC),
    schema_version="1.0.0",
)
DatasetLineageRecorder(writer=lineage).register(node=node)
catalog = DatasetRegistryService(lineage=lineage, registry=registry)
result = catalog.register(
    node=node,
    name="Interview Q&A",
    owner_id="evaluation-team",
    tags=("curated", "training"),
)
assert result.created
assert not catalog.register(
    node=node, name="Interview Q&A", owner_id="evaluation-team",
    tags=("training", "curated"),
).created
assert catalog.list_by_tag(tag="training") == (result.entry,)
```

## Guarantees

- Exact replays are idempotent, including tag order normalization.
- Dataset version numbers use numeric MAJOR.MINOR/PATCH order, not
  lexicographic string order. New versions must advance beyond the latest;
  unchanged replay of an older version is allowed.
- Once a version has been registered, changing its name, metadata, tags,
  digest or ownership is a conflict. Publish a new version instead.
- The metadata row, tag projection, and registration audit event commit in
  one SQLite `BEGIN IMMEDIATE` transaction. Concurrent exact registration
  creates one event. Injected audit failures roll everything back.
- Tag indexes are checked against canonical entry tags on every read;
  stored JSON SHA-256 checksums are verified before reconstruction.
- Query bounds are explicit (1–1000). Validation is fail-closed.

## Limitations and separate next steps

- Local SQLite is not PostgreSQL high availability or an immutable,
  independently signed audit store.
- Lineage and registry files are separate transaction boundaries: they
  cannot atomically commit together. Register lineage first, then catalog.
  A failed catalog registration may leave a lineage-only revision.
- No RBAC or tenant-scoped authorization is offered here. Do **not**
  expose write operations as unauthenticated FastAPI endpoints.
- Owner identifiers are caller-supplied metadata, **not** verified identity.
  Do not use emails or secrets as IDs, tags or descriptions.
- Artifact storage, object-store consistency, retention/GDPR erasure,
  schema registration checks, pagination cursors, HTTP management APIs
  and UI are future increments requiring authenticated composition.
- The registry does not claim distributed atomic publication or full
  enterprise production certification.

## Verification

```bash
uv run ruff check .
uv run pyright
uv run pytest -q
```

Regression tests cover lineage enforcement, idempotency, numeric semver
ordering, immutable metadata conflicts, bounded tag lookups, SQLite restart,
concurrent registration, checksum corruption, projection drift and injected
audit-write failures.
