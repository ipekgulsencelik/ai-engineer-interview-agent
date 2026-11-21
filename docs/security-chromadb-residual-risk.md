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
