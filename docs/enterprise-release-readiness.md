# Enterprise Release Readiness — source integrity, security gates and rollback

**Status:** Opt-in release-candidate pipeline with explicit fail-closed
checks. No registry image is published, and no Kubernetes or Docker
production deployment occurs automatically. A green CI check is *not*
an independently approved production release.

## Release workflow

New `.github/workflows/release-gate.yml` runs on versioned Git tags
(`vMAJOR.MINOR.PATCH`) and optionally by manual workflow dispatch for
dry-run validation. A candidate must match the `[project].version` in
`pyproject.toml` (currently `0.1.0`), checkout SHA, and a commit
reachable from `origin/main`. Tagged releases also verify the actual
tag ref resolves to the checked-out commit. Use a protected release-tag
ruleset; tag matching is not signature verification or approval.

The workflow includes five independent jobs:

1. **Source integrity** — verify version/source, archive the exact Git
   tree as an un-timestamped gzip bundle using `git archive`, generate
   SHA-256 manifest and a second byte-for-byte reproducibility check.
   Export CycloneDX runtime SBOM from the existing `uv.lock` using
   `uv export --locked --no-dev`. Publish those as GitHub artifacts.
2. **Runtime dependency audit** — export pinned runtime dependencies
   and run `pip-audit --strict --no-deps`. A reported advisory or failed
   vulnerability lookup blocks release; there is no `|| true`.
   The optional PostgreSQL/telemetry requirements have independent version
   ranges, not hashes; include them in the deployed lock/provenance
   before claiming full runtime dependency audit coverage.
3. **Container build + HIGH/CRITICAL scan** — build
   `Dockerfile.release` locally and scan the **built image** with Trivy.
   HIGH/CRITICAL OS and library vulnerabilities block release. No
   image is pushed and no registry credentials are requested. The
   Trivy action is pinned to a specific reviewed, post-incident Git
   commit SHA rather than a mutable tag. Third-party actions and
   base-image digests still require periodic independent review.
4. **Source provenance** — GitHub signed artifact attestation for
   the verified source bundle, using minimal scoped `id-token` and
   `attestations:write` permissions only in the attestation job.
5. **Release-ready check** — depends on *all previous jobs* and targets
   GitHub environment `production-release`. This only records
   readiness, **it does not deploy**.

**IMPORTANT:** GitHub can create an environment automatically without
approval rules. Configure `production-release` with trusted required
reviewers, prevent self-approval where supported, and restrict environment
branches/tags in **Settings → Environments**. Also configure protected
`main`, required CI status checks, signed/controlled tags and
CODEOWNERS-required reviews. Repo files alone do not enable
organization-level branch protection.

## Reproducible release bundle

The build script runs with `RELEASE_TAG` and `GITHUB_SHA` set from
verified GitHub metadata:

```bash
export RELEASE_TAG=v0.1.0
export GITHUB_SHA="$(git rev-parse HEAD)"
bash ops/release/build_bundle.sh
```

This produces:
- `dist/ai-engineer-interview-agent-v0.1.0.tar.gz`
- `dist/release-manifest.json`
- `dist/release-sha256sums.txt`

The tarball includes the tracked source tree but excludes tracked
Chroma database caches via `.gitattributes`. Its manifest records
the Git SHA, release tag/version, archive SHA-256, and uv.lock SHA-256.
Check that the archive and lock hashes match **after downloading**
and before any deployment. A source bundle is **not** an executable
container; it does not identify a specific built-image digest.

The release workflow produces a CycloneDX runtime SBOM in addition to
the archive. SBOM generation is not vulnerability scanning; the
separate dependency and image-scanning jobs are required.

Verify GitHub attestation with the GitHub CLI after a successful release:

```bash
gh attestation verify \
  dist/ai-engineer-interview-agent-v0.1.0.tar.gz \
  -R ipekgulsencelik/ai-engineer-interview-agent
```

## Production container security

`Dockerfile.release` is **separate from the existing development
Dockerfile**, avoiding disruption to developer workflows. It installs
the locked runtime dependency graph without development extras, runs
under numeric UID/GID `10001:10001`, and includes a simple HTTP
liveness check. `.dockerignore` excludes credentials, local
environments, Python caches, tests, monitoring ops files, and tracked
Chroma database volumes.

**Limitations:**
- The base image is still a version tag; production must replace it
  with a reviewed **immutable SHA-256 digest**.
- `pip install uv` uses a constrained version range rather than a
  hash-pinned wheel. For SLSA/provenance-grade hermetic builds, pin
  exact uv wheel hashes and your approved build platform.
- The container health check tests API liveness, **not** PostgreSQL,
  Groq, retrieval stores, downstream dependency readiness or a
  measured SLO. Add a distinct readiness contract before a live rollout.
- The production image is not created by the PR-only CI job; the
  tag/dispatch workflow actually builds and scans it.
- Prometheus, Barman Cloud backup plugin and PostgreSQL optional
  Python requirements are **not fully pinned** in the core lock.
  Their production image, security scan and provenance need separate
  coverage if they are part of the deployed topology.
- The existing local Compose bind mount `./data:/app/data` may need
  ownership `10001:10001` when using the production Dockerfile.
  Do not force host-wide permission changes.

## Manual deployment / canary / rollback policy

Before deployment, obtain a real immutable image digest from a
**separately reviewed image-publishing pipeline**. Do not deploy a
tag-only image such as `:latest`. The release pipeline deliberately
does not publish an image. Record the previous known-good digest
separately; it must not match the proposed digest.

`ops/release/release-plan.example.json` is intentionally invalid by
default. Replace placeholders only with independently verified
releases and evidence, and obtain approved security/operations/database
migration sign-off. Evaluate the documented plan with:

```bash
python -m src.infrastructure.operations.release_cli preflight \
  --plan /secure/path/to/verified-release-plan.json
```

Exit codes: `0` = self-reported evidence complete, `1` = unmet
checks, `2` = malformed/unreadable evidence. **The JSON booleans
are NOT authenticators:** anyone who can edit the JSON can set them
to true. The real authorization gate must independently verify checks
and require protected-environment approval/actor identity.

Recommended canary process, performed by an authorized operator:
1. Verify image SHA-256, artifact attestation, current SBOM, dependency
   audit, image scan, complete PR CI, cluster health, tenant RLS,
   recent **actual** offsite base backup and archived WAL.
2. Confirm the exact PostgreSQL Alembic revision and migration
   compatibility before traffic. For additive schema changes, use
   expand/migrate/contract so an older application can still run.
3. Deploy a single canary with low initial traffic. Compare request
   error ratio, p95/p99 latency, outbox retries, database replication
   lag and tenant access denials against an **approved baseline**.
4. Expand traffic only after controlled observation and explicit
   approval. A successful HTTP liveness probe alone is insufficient.
5. On regression, **stop expansion**, revert workload to the previous
   verified image digest and observe service health and queue
   idempotency. Do NOT roll back database migrations automatically.
6. If database data integrity was compromised, invoke the separate
   approved PITR and disaster-recovery runbook. A restore needs
   ownership, RPO/RTO verification, isolation and explicit cutover;
   it is not the same as application image rollback.
7. Document evidence timestamps, the release SHA, image digest,
   reviewer identity, exceptions and a post-release incident review.

## Outstanding production gates

- No live Kubernetes cluster or container registry is configured here.
- No published/proven signed image digest or deployed SLSA provenance.
- No verified end-to-end canary and rollback drill.
- No calibrated application SLO baselines or real readiness endpoint.
- No automated tenant-aware authorization regression test under live
  production identity.
- No image/platform SBOM for the optional PostgreSQL/OTel components.
- No completed restore from the actual cloud archive / HA failover under
  production NetworkPolicies.
- No independently managed release reviewer approvals or protected tag
  rules are configured from this repository change.

These are explicit blockers to calling the project fully
production-certified or Enterprise-Level available. This PR provides
release-candidate **controls**, not a production deployment.
