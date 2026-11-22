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
    assert "*.sh text eol=lf" in attributes


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
    # A binary pipe prevents subprocess text mode from restoring CRLF on Windows.
    result = subprocess.run(
        ["bash", "-n", "-"],
        input=path.read_bytes().replace(b"\r\n", b"\n"),
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr.decode(
        "utf-8", errors="replace"
    )
    script = path.read_text(encoding="utf-8")
    assert "git archive" in script
    assert "gzip -n" in script
    assert "cmp " in script
    assert "create-manifest" in script
    assert "verify-manifest" in script
    assert "sha256sum" in script
