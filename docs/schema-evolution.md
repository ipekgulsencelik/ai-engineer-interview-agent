# Dataset Schema Evolution (Phase 2)

The `src.evaluation.dataset.schema_evolution` package provides **explicit
versioned schemas for serialized dataset records**. Schema versions are independent
of `DatasetVersion.version`: changing dataset contents is not the same as changing
the shape of a record.

## Supported behavior

- Immutable schema definitions with strict `MAJOR.MINOR.PATCH` versions.
- Top-level JSON-compatible kinds: `string`, `integer`, `number`, `boolean`,
  `object`, and `array`. Nested object/array contents are **not** recursively
  typed in this first implementation.
- Strict record validation: missing required fields, unexpected fields, invalid
  types, unsupported nulls, and non-finite numeric values are rejected.
- Backward compatibility analysis determines whether **old records can be read
  by the new strict schema**. Consequently removal of a field is considered
  breaking, even if it was optional.
- Explicit, forward-only, linear migration chains. Adding a field may be
  compatible, but promoting records to a new schema version still requires
  an auditable migration step (it may have zero operations).
- Migrations receive copies of records. A failed batch raises an error; the
  service returns no partially migrated batch and does not mutate inputs.

## Example

```python
from src.evaluation.dataset.schema_evolution import (
    DatasetField,
    DatasetRecordSchema,
    MigrationRegistry,
    MigrationStep,
    RenameField,
    SchemaCompatibilityChecker,
    SchemaEvolutionService,
)

v1 = DatasetRecordSchema(
    name="interview_samples",
    version="1.0.0",
    fields=(DatasetField("answer", "string"),),
)
v2 = DatasetRecordSchema(
    name="interview_samples",
    version="2.0.0",
    fields=(DatasetField("candidate_answer", "string"),),
)

report = SchemaCompatibilityChecker().compare(source=v1, target=v2)
assert not report.backward_compatible

registry = MigrationRegistry([
    MigrationStep(
        from_version="1.0.0",
        to_version="2.0.0",
        operations=(RenameField("answer", "candidate_answer"),),
    )
])
result = SchemaEvolutionService(migrations=registry).migrate_records(
    records=[{"answer": "A retrieval-augmented response"}],
    source_schema=v1,
    target_schema=v2,
)
assert result == ({"candidate_answer": "A retrieval-augmented response"},)
```

## Integration boundary

The package deliberately operates on serialized record mappings and **does not
rewrite existing immutable `EvaluationDataset` aggregates or silently update their
`dataset_version`**. A caller can project serialized samples using
`EvaluationDatasetSerializer`, explicitly define a record schema, migrate the
record mappings, and then validate/rebuild domain entities through existing
loaders/constructors. End-to-end aggregate reconstruction, persistent schema
registries, lineage, rollback and nested schema evolution are future work.

## SOLID contracts

`DatasetRecordValidator` validates; `SchemaCompatibilityChecker` compares;
`MigrationRegistry` resolves; `SchemaEvolutionService` orchestrates.
The service depends on `RecordValidationPort` and `MigrationPathResolver`
protocols. Custom migration operations implement `MigrationOperation` without
modifying the orchestration service.

## Quality gates

```bash
uv run ruff check .
uv run pyright
uv run pytest -q
```
