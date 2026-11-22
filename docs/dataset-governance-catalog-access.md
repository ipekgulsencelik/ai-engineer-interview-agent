# Phase 2 — Dataset Catalog Governance (read-only foundation)

This increment introduces a **read-only catalog metadata access boundary**.
It extends the existing Dataset Registry without changing the registry
schema, storing raw dataset artifacts, or opening an unauthenticated HTTP API.

## Request path

`GovernedDatasetCatalogReader.get(revision)`:

1. Gets a trusted principal through the injected `VerifiedIdentityPort`.
2. Resolves a separately administered `CatalogAccessPolicy` through
   `CatalogPolicyPort`; never trusts the catalog's `owner_id` for access.
3. Checks tenant equality and an explicit allowed role set. No allow policy
   means deny. The minimal roles are `reader` and `steward`; both require
   explicit authorization by the separate policy store.
4. Denies catalog metadata access at or after `access_expires_at`, if set.
   Expiry is a **read-access cutoff**, not automatic deletion or proof that a
   legal retention period has elapsed.
5. Calls the underlying `RegistryReader.get` **only after authorization**.
6. Writes a metadata-only access decision to `CatalogAuditPort`. The event
   must commit successfully **before** the result is released.
7. Returns the catalog entry only after a successful allowed audit event.
   Unauthorized and missing entries raise the same outward-facing
   `DatasetCatalogAccessDenied` exception, avoiding existence disclosure.

This is application-layer authorization, not authentication or a universal
policy decision point. The identities must be created only from verified
authentication sessions, not JSON request bodies, unverified JWT claims,
headers, or user-supplied role lists.

## Durable audit

`SQLiteDatasetGovernanceAuditRepository` provides append-only
`CatalogAccessAuditEvent` records (event ID, opaque principal ID, tenant ID,
dataset revision, timestamp, reason code, allowed). SHA-256 checksums detect
accidental payload changes and check the indexed row against the canonical
payload. Duplicate event IDs fail rather than replacing records. The SQLite sort key
normalizes timestamps to UTC with a fixed microsecond precision, ensuring
correct bounded ordering across timezone offsets; original event timestamps
remain in the canonical checksummed JSON payload.

**This is not a tamper-proof audit store.** Administrators with write access
to local SQLite can rewrite both payloads and checksums. Production-grade
audit immutability requires external append-only storage, signing, retention
configuration, backup/recovery tests, and independent access controls.

Log principal IDs must be opaque and nonidentifying. Never use emails,
secrets, raw interview questions, personal answers, CV content, or tokens as
identifiers. Audit reads must be restricted; no HTTP routes expose this store.

## SOLID / Clean Architecture

- Domain/application: `src/evaluation/dataset/governance.py`.
- Injected ports: `VerifiedIdentityPort`, `CatalogPolicyPort`,
  `CatalogAuditPort`, `RegistryReader`, `CatalogClock`.
- Infrastructure adapter:
  `src/infrastructure/repositories/sqlite_dataset_governance_audit_repository.py`.
- Existing registry's internal API is **not** automatically secured by this
  facade. An authenticated composition root must inject only the governed
  reader into untrusted request paths and keep the raw `RegistryReader`
  inaccessible there.

No new ACL/tenant table or policy mutation endpoint is included. Runtime
policy storage, policy administration authorization, verified identity
integration, cross-tenant security tests under a deployed API, physical
retention and erasure, legal holds, artifact-level access, audit chain
anchoring and production review are independent follow-up work.

## Tests

```bash
uv run ruff check .
uv run pyright
uv run pytest -q tests/evaluation/dataset/test_governance_catalog.py
uv run pytest -q
```

No application deployment or broader release approval is implied by these
tests. Production-image vulnerability gates tracked in Issue #47 remain
separate.
