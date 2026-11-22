# Dataset Registry → Quality Engine Gate

The `RegisteredDatasetQualityGate` is an application orchestration service.
It connects an existing immutable catalog revision to the existing quality
evaluator and report storage without adding a second validation engine.

## Architecture

- `RegistryReader` resolves an existing catalog revision and its exact SHA-256.
- The caller supplies the immutable artifact as **bytes**.
- SHA-256 is verified **before** the decoder is invoked.
- An injected `DatasetArtifactDecoder` parses **those same verified bytes** into records.
- The existing `QualityEvaluatorPort` evaluates the decoded records.
- A report with a different dataset ID/version is rejected before persistence.
- The `QualityReportStorePort` persists the passing or failing report.
  Policy acceptance (`report.accepted`) is not overwritten.

These interfaces allow unit tests without SQL or remote APIs. The application
layer does not depend on the SQLite adapter or a specific artifact codec.

## Security and limits

SHA-256 establishes byte equality against the catalog digest, not independent
publisher authentication. The decoder must be trusted, bounded, and chosen
for the dataset format; it is deliberately injected rather than assuming all
published artifacts are JSON. Artifact bytes and decoded records are not
written to the registry. There is no new unauthenticated HTTP endpoint.
Cross-store publication, evaluation and report persistence are **not** one
atomic transaction. Concurrency, retention, tenant authorization and object
storage lifecycle require separate production controls.

This branch is stacked on `feat/phase2-dataset-registry-versioning`; merge
the dependency first after its independent review and protection gates.

## Tests

```bash
uv run ruff check src/evaluation/dataset/quality/registry_gate.py tests/evaluation/dataset/quality/test_registry_gate.py
uv run pyright
uv run pytest -q tests/evaluation/dataset/quality/test_registry_gate.py
```
