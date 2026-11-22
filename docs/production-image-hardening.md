# Production Docker image hardening (candidate only)

## Threat model and changes

The production image now has two stages based on the **same Python image
distribution**. A builder installs uv and resolves the locked production-only
dependency graph. The runtime receives only the Python virtual environment
and root-owned application source, not the build-only uv tooling.
The system-level pip/setuptools/wheel packaging entrypoints are uninstalled
from the final runtime. The runtime is an unprivileged numeric user
(`10001:10001`), with a private writable `/app/data` (mode 0700).
The application source and environment are not writable by this user.

Both stages intentionally use the same Python ABI and distribution to avoid
incompatible native-extension dependencies (PyTorch, sentence-transformers).

The build context excludes local Chroma files, SQLite indexes and their
WAL/SHM/snapshot variants, secrets, tests and CI files. A fresh question-vector
index must be built or supplied separately from trusted input after deployment.

## Verification (no image publication)

Run the project CI, then build with Docker:

```bash
docker build --pull -f Dockerfile.release -t ai-interview-candidate:local .
docker image inspect --format '{{.Config.User}}' ai-interview-candidate:local
docker run --rm --entrypoint /app/.venv/bin/python ai-interview-candidate:local \
  -c "import importlib.util; assert importlib.util.find_spec('pip') is None"
```

The Python packaging test above checks isolation only if importlib is using
the default environment; it is **not a substitute for an OS vulnerability
scan**. Use the blocking Trivy HIGH/CRITICAL, pip-audit --strict and release
workflow. CI must verify source provenance, dependencies and runtime health.

## Outstanding blockers

- Ordinary PR CI still builds from a mutable base for development. The
  **release-gate** now requires `APPROVED_PYTHON_BASE_IMAGE` to be a fully
  qualified `docker.io/library/python:3.11-slim-trixie@sha256:<64-hex>`
  GitHub Actions repository variable. If unset or malformed it fails before
  building. Operations must independently verify upstream provenance, the
  **multi-platform manifest digest**, current OS advisories and supported
  architecture before setting the value. Syntax validation is not approval.
- Debian/OS vulnerabilities may remain in the Python runtime layer even
  after removing the build tools. Do not waive Trivy findings.
- Test actual container startup, embedded SQLite data access and
  sentence-transformers native-library imports with pre-staged reviewed
  model weights before operator acceptance.
- A read-only root filesystem, network egress policy, resource limits,
  backup/restore and model revision allowlist require deployment-level
  enforcement; Dockerfile configuration alone does not provide them.
- Never deploy or publish directly from this PR. Keep all release security
  gates mandatory and require independent reviewer/operator approval.

## Immutable release base-image control

The production release workflow reads GitHub Actions repository variable
`APPROVED_PYTHON_BASE_IMAGE`. Set it only to an independently verified
official multi-platform digest reference of the form
`docker.io/library/python:3.11-slim-trixie@sha256:<reviewed-64-hex>`.
Do not use the example placeholders as values; an unauthorized or missing
setting prevents the release container build.

The policy is intentionally strict to detect tag-only, wrong-runtime,
wrong-distribution and alternate-registry inputs. Existing PR CI continues to
run without requiring this release approval variable. The release workflow
passes the exact approved value to both image build stages.

**This control does not certify the digest, solve HIGH/CRITICAL image
vulnerabilities or authorize deployment.** Confirm signatures/provenance and
blocking security scans independently.


## Continuous pull-request vulnerability gate

The separate `.github/workflows/production-image-pr-security.yml` runs on
every pull request targeting `main` or `develop`, not only on a release
tag. It blocks on known production dependency advisories using locked
`pip-audit --strict` and on HIGH/CRITICAL OS and library advisories in the
**actual** `Dockerfile.release` built image using Trivy. There are no
`ignore-unfixed` exemptions or auto-publish steps.

**Important:** Even a green application CI does not imply a releasable
container. Until the 51 HIGH CVE findings in the existing production image
are remediated, this new security check is expected to fail deliberately.

A GitHub repository administrator must configure branch protection or a
ruleset for `main` and `develop` requiring both checks by their exact
names: `Locked production dependency audit` and
`Production image HIGH/CRITICAL gate`. Also require the existing
`Ruff + Pyright + Pytest` check, an approving review, up-to-date branches,
and block force pushes/deletions. On 2026-11-22 `main` was not protected
and the repository returned no active rulesets. These GitHub admin controls
cannot be enforced merely by committing a workflow.


## Issue #47 — independent CVE review and audit artifacts

See [runtime CVE triage](security/issue-47-runtime-cve-triage.md) for
version-specific evidence and the release-blocking Debian 12/13 advisories.
In particular, a missing `gz_vacate()` symbol does not establish that
the Bookworm zlib HIGH advisory is a false positive; Debian maintainers
reported a related crash in older code.

The PR security workflow stores `trivy-image-findings.json` as a
30-day GitHub Actions artifact even when the scanner returns a failure.
It also records the unsuppressed HIGH/CRITICAL totals in the run summary.
The JSON report is audit evidence, not a waiver; scanner exit code 1 and
all original mandatory release checks remain unchanged.
