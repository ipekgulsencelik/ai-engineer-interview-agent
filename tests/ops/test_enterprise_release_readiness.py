"""Release version, provenance and operator-approval gates."""

from __future__ import annotations

import copy
import io
import json
import subprocess
import sys
import tarfile
from pathlib import Path

import pytest

from src.application.release.readiness import ReleaseReadinessEvaluator
from src.infrastructure.operations.release_cli import (
    create_bundle_manifest,
    release_version,
    verify_bundle_manifest,
    verify_source_commit,
)


def approved() -> dict:
    prefix = "ghcr.io/ipekgulsencelik/ai-engineer-interview-agent@sha256:"
    return {
        "version": "v0.1.0",
        "source_sha": "a" * 40,
        "image": prefix + "a" * 64,
        "rollback_image": prefix + "b" * 64,
        "approvals": {
            "security_reviewed": True,
            "operations_approved": True,
            "database_migration_reviewed": True,
        },
        "evidence": {
            "ci_green": True,
            "dependency_audit_passed": True,
            "container_scan_passed": True,
            "sbom_recorded": True,
            "backup_restore_tested": True,
            "rollback_drill_verified": True,
        },
    }


def test_valid_plan_is_documented_but_not_an_authority() -> None:
    decision = ReleaseReadinessEvaluator().evaluate(approved())
    assert decision.allowed
    assert decision.failed_checks == ()
    assert "independent" in decision.to_dict()["assurance"]


@pytest.mark.parametrize(
    ("key", "value"),
    [
        ("version", "v0.1"),
        ("version", "v01.2.3"),
        ("version", "v0.1.0-beta"),
        ("source_sha", "123"),
        ("source_sha", "b" * 64),
        ("image", "ghcr.io/example/app:latest"),
        ("image", "docker.io/other/app@sha256:" + "c" * 64),
        ("image", "ghcr.io/example/app@sha256:REPLACE"),
        ("rollback_image", "ghcr.io/example/app:previous"),
    ],
)
def test_invalid_release_identity_fails_closed(
    key: str, value: str
) -> None:
    plan = approved()
    plan[key] = value
    assert not ReleaseReadinessEvaluator().evaluate(plan).allowed


def test_reusing_current_digest_is_not_a_rollback_plan() -> None:
    plan = approved()
    plan["rollback_image"] = plan["image"]
    result = ReleaseReadinessEvaluator().evaluate(plan)
    assert "distinct_rollback_image_digest" in result.failed_checks


@pytest.mark.parametrize("section", ["approvals", "evidence"])
def test_all_operator_and_security_evidence_is_required(
    section: str
) -> None:
    plan = approved()
    for field in plan[section]:
        test_plan = copy.deepcopy(plan)
        test_plan[section][field] = False
        decision = ReleaseReadinessEvaluator().evaluate(test_plan)
        assert not decision.allowed
        assert f"{section}.{field}" in decision.failed_checks


@pytest.mark.parametrize("bad", [None, "true", 1, [], {}])
def test_bool_evidence_cannot_be_spoofed(bad: object) -> None:
    plan = approved()
    plan["evidence"]["ci_green"] = bad
    assert not ReleaseReadinessEvaluator().evaluate(plan).allowed


def test_decision_does_not_leak_extra_plan_metadata() -> None:
    plan = approved()
    plan["database_dsn"] = "SUPERSECRET_DATABASE"
    decision = ReleaseReadinessEvaluator().evaluate(plan)
    assert "SUPERSECRET_DATABASE" not in str(decision.to_dict())


def _source(tmp_path: Path) -> tuple[Path, Path, Path]:
    project = tmp_path / "pyproject.toml"
    project.write_text('[project]\nversion = "0.1.0"\n', encoding="utf-8")
    lock = tmp_path / "uv.lock"
    lock.write_text('version = 1\n', encoding="utf-8")
    archive = tmp_path / "source.tar.gz"
    with tarfile.open(archive, "w:gz") as out:
        for name, data in (
            ("pyproject.toml", project.read_bytes()),
            ("uv.lock", lock.read_bytes()),
            ("Dockerfile.release", b"USER 10001:10001"),
            ("src/api/app.py", b"app = None"),
        ):
            node = tarfile.TarInfo(name)
            node.size = len(data)
            out.addfile(node, io.BytesIO(data))
    return project, lock, archive


def test_version_must_match_pyproject(tmp_path: Path) -> None:
    project, _, _ = _source(tmp_path)
    assert release_version("v0.1.0", project) == "0.1.0"
    for tag in ("v0.1.1", "v01.1.0", "v1.0.0-rc1", "v0.1.0;rm -rf"):
        with pytest.raises(ValueError):
            release_version(tag, project)


def test_bundle_manifest_verifies_digest_and_git_source(tmp_path: Path) -> None:
    project, lock, archive = _source(tmp_path)
    record = create_bundle_manifest(
        archive=archive,
        project_file=project,
        lockfile=lock,
        tag="v0.1.0",
        commit="a" * 40,
    )
    verify_bundle_manifest(
        manifest=record,
        archive=archive,
        project_file=project,
        lockfile=lock,
        tag="v0.1.0",
        commit="a" * 40,
    )
    lock.write_text("tampered", encoding="utf-8")
    with pytest.raises(ValueError, match="checksum"):
        verify_bundle_manifest(
            manifest=record,
            archive=archive,
            project_file=project,
            lockfile=lock,
            tag="v0.1.0",
            commit="a" * 40,
        )


def test_bundle_rejects_hidden_env_secrets(tmp_path: Path) -> None:
    project, lock, archive = _source(tmp_path)
    with tarfile.open(archive, "w:gz") as out:
        for name in (
            "pyproject.toml", "uv.lock", "Dockerfile.release",
            "ops/secrets/.env.production",
        ):
            data = b"some value"
            node = tarfile.TarInfo(name)
            node.size = len(data)
            out.addfile(node, io.BytesIO(data))
    with pytest.raises(ValueError, match="environment"):
        create_bundle_manifest(
            archive=archive, project_file=project,
            lockfile=lock, tag="v0.1.0", commit="a" * 40,
        )


def test_bundle_rejects_parent_path(tmp_path: Path) -> None:
    project, lock, archive = _source(tmp_path)
    with tarfile.open(archive, "w:gz") as out:
        for name in (
            "pyproject.toml", "uv.lock", "Dockerfile.release",
            "../private-credentials",
        ):
            data = b"x"
            node = tarfile.TarInfo(name)
            node.size = len(data)
            out.addfile(node, io.BytesIO(data))
    with pytest.raises(ValueError, match="unsafe path"):
        create_bundle_manifest(
            archive=archive, project_file=project,
            lockfile=lock, tag="v0.1.0", commit="a" * 40,
        )


def test_git_sha_mismatch_is_rejected_before_ancestry_call(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        subprocess, "run",
        lambda *args, **kwargs: subprocess.CompletedProcess(
            args[0], 0, stdout="b" * 40 + "\n"
        ),
    )
    with pytest.raises(ValueError, match="checkout"):
        verify_source_commit(
            tag="v0.1.0",
            commit="a" * 40,
            pyproject=Path("pyproject.toml"),
            check_main=True,
        )


def test_cli_preflight_exit_code_communicates_blockers(tmp_path: Path) -> None:
    plan = approved()
    plan["approvals"]["security_reviewed"] = False
    plan_path = tmp_path / "plan.json"
    plan_path.write_text(json.dumps(plan), encoding="utf-8")
    command = [
        sys.executable,
        "-m", "src.infrastructure.operations.release_cli",
        "preflight", "--plan", str(plan_path),
    ]
    result = subprocess.run(
        command, capture_output=True, text=True,
        check=False, timeout=15,
    )
    assert result.returncode == 1
    assert "approvals.security_reviewed" in result.stdout
    assert "ghcr.io" not in result.stdout


def test_cli_refuses_corrupt_plan_without_echoing_credentials(
    tmp_path: Path,
) -> None:
    plan = tmp_path / "production.json"
    plan.write_text('{"password":"SECRET_PASSWORD"}', encoding="utf-8")
    result = subprocess.run(
        [
            sys.executable,
            "-m", "src.infrastructure.operations.release_cli",
            "preflight", "--plan", str(plan),
        ],
        capture_output=True, text=True, check=False, timeout=15,
    )
    assert result.returncode == 1
    assert "SECRET_PASSWORD" not in result.stdout + result.stderr
