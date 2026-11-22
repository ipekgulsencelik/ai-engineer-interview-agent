"""Static security boundaries for the gated, no-deploy release workflow."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

import pytest

yaml = pytest.importorskip("yaml")
ROOT = Path(".")


def _release_workflow() -> dict:
    data = yaml.safe_load(
        (ROOT / ".github/workflows/release-gate.yml").read_text(
            encoding="utf-8"
        )
    )
    assert isinstance(data, dict)
    return data


def test_release_requires_source_audit_image_and_attestation() -> None:
    workflow = _release_workflow()
    assert workflow["permissions"] == {"contents": "read"}
    assert workflow["concurrency"]["cancel-in-progress"] is False
    jobs = workflow["jobs"]
    assert set(jobs) == {
        "source-integrity",
        "dependency-audit",
        "container-scan",
        "provenance",
        "release-ready",
    }
    assert set(jobs["release-ready"]["needs"]) == {
        "source-integrity",
        "dependency-audit",
        "container-scan",
        "provenance",
    }
    assert jobs["release-ready"]["environment"] == "production-release"
    assert jobs["provenance"]["permissions"] == {
        "contents": "read", "id-token": "write", "attestations": "write"
    }


def test_release_scanners_are_mandatory_and_no_deploy_occurs() -> None:
    workflow = _release_workflow()
    jobs = workflow["jobs"]
    audit = str(jobs["dependency-audit"]["steps"])
    assert "pip-audit" in audit
    assert "--strict" in audit
    assert "--no-dev" in audit
    scan = str(jobs["container-scan"]["steps"])
    assert "Dockerfile.release" in scan
    assert re.search(
        r"aquasecurity/trivy-action@[a-f0-9]{40}", scan
    )
    assert "CRITICAL,HIGH" in scan
    assert "'1'" in scan or '"1"' in scan
    release = str(jobs["release-ready"]["steps"])
    assert "No deployment" in release
    for dangerous in ("docker push", "kubectl apply", "helm upgrade"):
        assert dangerous not in str(jobs)


def test_attestation_binds_to_source_archive_not_a_mutable_tag() -> None:
    workflow = _release_workflow()
    source = str(workflow["jobs"]["source-integrity"]["steps"])
    assert "verify-source" in source
    assert "--check-main" in source
    assert "--check-tag-ref" in source
    assert "build_bundle.sh" in source
    assert "cyclonedx1.5" in source
    provenance = str(workflow["jobs"]["provenance"]["steps"])
    assert "attest@" in provenance
    assert "subject-path" in provenance
    assert "*.tar.gz" in provenance


def test_container_runs_as_numeric_nonroot_and_excludes_secrets() -> None:
    dockerfile = (ROOT / "Dockerfile.release").read_text()
    assert "USER 10001:10001" in dockerfile
    assert "uv sync --frozen --no-dev --no-install-project" in dockerfile
    assert "HEALTHCHECK" in dockerfile
    assert "src.api.app:app" in dockerfile
    ignore = (ROOT / ".dockerignore").read_text()
    for part in (
        ".env.*", "**/.env.*", ".git/", ".venv/",
        "data/chroma/", "*.pem", "*.key", "tests/",
    ):
        assert part in ignore
    attributes = (ROOT / ".gitattributes").read_text()
    assert "data/chroma/" in attributes
    assert "export-ignore" in attributes


def test_dependabot_targets_uv_lockfile_and_immutable_review_paths() -> None:
    deps = yaml.safe_load(
        (ROOT / ".github/dependabot.yml").read_text()
    )
    assert deps["version"] == 2
    assert {
        item["package-ecosystem"] for item in deps["updates"]
    } == {"uv", "docker", "github-actions"}
    owners = (ROOT / ".github/CODEOWNERS").read_text()
    assert "/.github/workflows/" in owners
    assert "/Dockerfile.release" in owners
    assert "/ops/postgres-ha/" in owners


def test_example_release_plan_is_explicitly_not_approved() -> None:
    from src.application.release.readiness import ReleaseReadinessEvaluator

    example = json.loads(
        (ROOT / "ops/release/release-plan.example.json").read_text(
            encoding="utf-8"
        )
    )
    result = ReleaseReadinessEvaluator().evaluate(example)
    assert not result.allowed
    assert "immutable_image_digest" in result.failed_checks
    assert "approvals.security_reviewed" in result.failed_checks


def test_release_build_script_has_syntax_and_reproducibility_checks() -> None:
    path = ROOT / "ops/release/build_bundle.sh"
    result = subprocess.run(
        ["bash", "-n", str(path)],
        check=False, capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stderr
    script = path.read_text(encoding="utf-8")
    assert "git archive" in script
    assert "gzip -n" in script
    assert "cmp " in script
    assert "create-manifest" in script
    assert "verify-manifest" in script
    assert "sha256sum" in script


def test_release_image_has_separate_builder_and_nonroot_runtime() -> None:
    """Build-only dependency tools and user-writable state are isolated."""
    dockerfile = (ROOT / "Dockerfile.release").read_text(encoding="utf-8")
    assert dockerfile.count("FROM ${PYTHON_IMAGE}") == 2
    builder, runtime = dockerfile.split("FROM ${PYTHON_IMAGE} AS runtime")
    assert "AS builder" in builder
    assert "uv sync --frozen --no-dev --no-install-project" in builder
    assert "pip install" in builder
    assert "pip install" not in runtime
    assert "COPY --from=builder /app/.venv /app/.venv" in runtime
    assert "pip uninstall --yes pip setuptools wheel" in runtime
    assert "chmod 0700 /app/data" in runtime
    assert "USER 10001:10001" in runtime


def test_production_image_context_rejects_local_sqlite_state() -> None:
    """Secret/snapshot/index material must not enter the build context."""
    ignore = (ROOT / ".dockerignore").read_text(encoding="utf-8")
    for pattern in (
        "data/**/*.sqlite3",
        "data/**/*.sqlite3-*",
        "data/**/*.sqlite3.*",
        "data/**/*.db",
        "data/**/*.db-*",
        "data/**/*.db.*",
    ):
        assert pattern in ignore



def test_release_build_requires_explicit_immutable_base_image_digest() -> None:
    workflow = _release_workflow()
    steps = workflow["jobs"]["container-scan"]["steps"]
    names = [step.get("name", "") for step in steps]
    require_index = names.index("Require approved immutable Python base-image digest")
    build_index = names.index("Build candidate image locally")
    assert require_index < build_index
    assert "verify_release_base_image" in str(steps[require_index]["run"])
    build = str(steps[build_index])
    assert "APPROVED_PYTHON_BASE_IMAGE" in build
    assert "--build-arg" in build
    assert "PYTHON_IMAGE=" in build
    assert "vars.APPROVED_PYTHON_BASE_IMAGE" in build


def test_production_image_security_runs_for_every_pr_without_waivers() -> None:
    """Security gate must be blocking on normal PRs, not only release tags."""
    workflow = yaml.safe_load(
        (ROOT / ".github/workflows/production-image-pr-security.yml").read_text(
            encoding="utf-8"
        )
    )
    assert workflow["permissions"] == {"contents": "read"}
    triggers = workflow.get("on", workflow.get(True))
    assert set(triggers["pull_request"]["branches"]) == {"main", "develop"}
    assert "paths" not in triggers["pull_request"]
    jobs = workflow["jobs"]
    assert set(jobs) == {"locked-runtime-audit", "production-image-scan"}
    audit = str(jobs["locked-runtime-audit"]["steps"])
    assert "uv export --locked --no-dev" in audit
    assert "pip-audit --no-deps --strict" in audit
    assert "chromadb" in audit
    scan = jobs["production-image-scan"]["steps"]
    assert "Dockerfile.release" in str(scan)
    trivy = next(step for step in scan if "trivy-action@" in step.get("uses", ""))
    assert re.search(r"aquasecurity/trivy-action@[a-f0-9]{40}", trivy["uses"])
    assert trivy["with"]["exit-code"] == "1"
    assert trivy["with"]["severity"] == "CRITICAL,HIGH"
    assert trivy["with"]["vuln-type"] == "os,library"
    assert trivy["with"]["ignore-unfixed"] is False
    assert trivy["with"]["scanners"] == "vuln"
    assert "10001:10001" in str(scan)
    assert all("docker push" not in str(step) for step in scan)


def test_failed_image_scan_retains_machine_readable_evidence() -> None:
    """Independent reviewers must get the exact blocking Trivy result."""
    workflow = yaml.safe_load(
        (ROOT / ".github/workflows/production-image-pr-security.yml").read_text(
            encoding="utf-8"
        )
    )
    steps = workflow["jobs"]["production-image-scan"]["steps"]
    trivy = next(step for step in steps if "trivy-action@" in step.get("uses", ""))
    assert trivy["with"]["format"] == "json"
    assert trivy["with"]["output"] == "trivy-image-findings.json"
    assert trivy["with"]["exit-code"] == "1"
    assert trivy["with"]["ignore-unfixed"] is False
    summary = next(
        step
        for step in steps
        if step.get("name") == "Summarize unsuppressed vulnerability counts"
    )
    assert summary["if"] == "always()"
    assert "GITHUB_STEP_SUMMARY" in summary["run"]
    archive = next(
        step
        for step in steps
        if step.get("name") == "Preserve exact Trivy report for independent review"
    )
    assert archive["if"] == "always()"
    assert archive["with"]["path"] == "trivy-image-findings.json"
    assert archive["with"]["retention-days"] == 30
    assert re.fullmatch(
        r"actions/upload-artifact@[a-f0-9]{40}",
        archive["uses"].split()[0],
    ) is not None
