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

- The base image reference is currently mutable. Pin a **reviewed,
  verifiable, multi-platform SHA-256 manifest digest** in the release process.
  Avoid inventing a digest or relying on a tag's name as an integrity check.
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
