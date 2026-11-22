# ChromaDB residual vulnerabilities — deployment hardening and release block

Issue #47 and the real 2026-11-22 `pip-audit` run report several
**unpatched ChromaDB 1.5.9 advisories**, including tenant authorization
bypass and remote code execution via exposed Chroma server endpoints.
Upgrading to the newest installable version does **not** remove these
advisories. See
https://github.com/chroma-core/chroma/issues/7909 and upstream advisories.

## Current application-specific exposure

The repository's two infrastructure adapters create embedded local clients
with `chromadb.PersistentClient(path=...)`. The repository does **not**
configure a Chroma `HttpClient`, run the `chroma run` server process,
or publish the Chroma server's HTTP port. The production Dockerfile starts
FastAPI, not a standalone Chroma server.

**This limits exploitability of the specifically reported remote Chroma
server endpoints in this architecture**, but it does NOT patch ChromaDB's
code or prove all vulnerabilities are unreachable through other code paths.
FastAPI's own retrieval endpoints remain a separate application attack
surface. Do not attach an untrusted remote ChromaDB server to the current
code or use the embedded package for untrusted collection creation,
collection modification, model repository names or `trust_remote_code`.

## Release control — no automatic waiver

- Keep `pip-audit --strict` and the built-container Trivy
  HIGH/CRITICAL check **required**. Do not add `--ignore-vuln`,
  `|| true`, or blanket exceptions to release workflows.
- Restrict Chroma to a single-tenant/local, privately stored question bank
  until a patched and supported release exists or an alternative vector
  store is implemented behind the existing application `VectorStore` port.
- Do not deploy Chroma as a network-accessible service or reuse it as a
  multi-tenant persistence boundary. Existing PostgreSQL RLS controls do
  not isolate Chroma collections.
- Treat persisted Chroma SQLite/index files and question text as untrusted
  inputs for supply-chain and artifact-scanning purposes. Restrict on-disk
  directory permissions; never store patient, candidate or identity data
  in the shared question bank.
- Require a documented architecture-level security assessment, provenance
  review, configuration audit, and (preferably) an upstream fixed version
  before accepting an exception in any private environment.
- Production release remains **blocked** by unpatched Chroma advisories.
  CI green does not override the release security gate.

## Regression guardrails

The `test_chroma_local_only_deployment` suite confirms both infrastructure
client composition paths use embedded `PersistentClient`, verifies
no `HttpClient` / `CloudClient` Chroma constructor exists in infrastructure,
and checks production Docker and Compose do not publish a Chroma service.
These checks guard the current mitigation but are **not** a penetration
test or vulnerability remediation.

## Chroma-free retrieval migration (staged hardening)

The current FastAPI retrieval composition root now selects the embedded
`SqliteQuestionVectorStore` behind the existing application
`QuestionVectorStore` port. It stores complete, validated Question entities,
performs exact cosine-based retrieval with deterministic tie-breaking and
bound-parameter filtering, and rejects nonfinite or mismatched embeddings.
The store uses only the Python standard library and has a 50,000-record
capacity guard. It is an **exact scan**, not approximate nearest-neighbor
search; benchmark capacity and p95 latency before a production migration.

The default location is `data/question_vectors.sqlite3` and may be changed
with `QUESTION_VECTOR_DB_PATH`. Existing Chroma data is **not** imported,
interpreted, or implicitly trusted. Rebuild the index from the original,
trusted question dataset using `QuestionIndexingService` and verify embedding
model/dimension parity. A missing SQLite index is initially empty; it does
not silently fall back to Chroma. Plan backup, access control, and integrity
checks for the new local database before production rollout.

Legacy Chroma constructors now refuse staging/production environments. They
remain for isolated development/test compatibility, not remote service use.
**This change does not yet remove ChromaDB from the locked runtime dependency
set or resolve the OS-level Trivy findings. Release security gates remain
blocking** until dependency isolation, lockfile regeneration, independent
`pip-audit` and image scanning succeed.

The legacy environment guard is **opt-in, default disabled**:
`LEGACY_CHROMA_ENABLED=false` is the default in all environments.
Only an explicit `LEGACY_CHROMA_ENABLED=true` **and** `ENV=development`
or `ENV=test` permits constructing a legacy local client. Do not set
this flag on any deployment or expose the embedded persistence files to
untrusted users.

The default embedding provider composition is now wired with the lazy
SentenceTransformerModelLoader, retry executor, normalized embeddings and
configured batch size. Loading model weights remains an **explicit runtime
dependency**; a release must validate model supply-chain provenance and
pin a reviewed revision before accepting untrusted runtime environments.
