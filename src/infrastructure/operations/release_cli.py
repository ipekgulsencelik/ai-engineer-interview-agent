"""Reproducible release-source verification and approval-plan CLI.

No deployments, logins or registry mutations are performed. All output is
designed to avoid echoing source inputs or secret-bearing exception strings.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import tarfile
import tomllib
from pathlib import Path
from typing import Any

from src.application.release.readiness import ReleaseReadinessEvaluator

VERSION_PATTERN = re.compile(
    r"v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
)
COMMIT_PATTERN = re.compile(r"[0-9a-f]{40}")


def release_version(tag: str, project_file: Path) -> str:
    if VERSION_PATTERN.fullmatch(tag) is None:
        raise ValueError("release tag must be vMAJOR.MINOR.PATCH")
    with project_file.open("rb") as file:
        project = tomllib.load(file)
    version = project["project"]["version"]
    if not isinstance(version, str) or tag != f"v{version}":
        raise ValueError("release tag differs from pyproject version")
    return version


def verify_source_commit(
    *,
    tag: str,
    commit: str,
    pyproject: Path,
    check_main: bool = False,
    check_tag_ref: bool = False,
) -> None:
    release_version(tag, pyproject)
    if COMMIT_PATTERN.fullmatch(commit) is None:
        raise ValueError("commit must be a full lowercase Git SHA")
    actual = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    if actual != commit:
        raise ValueError("checkout does not match requested commit")
    if check_main:
        comparison = subprocess.run(
            ["git", "merge-base", "--is-ancestor", commit, "origin/main"],
            check=False,
            capture_output=True,
            timeout=15,
        )
        if comparison.returncode != 0:
            raise ValueError("release commit must be reachable from main")
    if check_tag_ref:
        # No shell interpolation of Git refs: version syntax is strict.
        value = subprocess.run(
            ["git", "rev-parse", f"refs/tags/{tag}^{{commit}}"],
            capture_output=True,
            text=True,
            check=True,
            timeout=15,
        ).stdout.strip()
        if value != commit:
            raise ValueError("tag points to a different commit")


def file_sha256(filename: Path) -> str:
    sha = hashlib.sha256()
    with filename.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            sha.update(block)
    return sha.hexdigest()


def create_bundle_manifest(
    *, archive: Path, project_file: Path, lockfile: Path,
    tag: str, commit: str,
) -> dict[str, str]:
    if COMMIT_PATTERN.fullmatch(commit) is None:
        raise ValueError("commit must be full Git SHA")
    version = release_version(tag, project_file)
    if not archive.is_file() or archive.stat().st_size == 0:
        raise ValueError("release archive is missing or empty")
    if not lockfile.is_file():
        raise ValueError("lockfile is missing")
    with tarfile.open(archive, "r:gz") as tar:
        names = set(tar.getnames())
        expected = {"pyproject.toml", "uv.lock", "Dockerfile.release"}
        if not expected.issubset(names):
            raise ValueError("release archive lacks required source files")
        for name in names:
            parts = Path(name).parts
            if name.startswith("/") or ".." in parts:
                raise ValueError("archive includes unsafe path")
            if (
                any(segment.startswith(".env") for segment in parts)
                and name not in (
                    ".env.example", "ops/observability/.env.example"
                )
            ):
                raise ValueError("archive includes an environment file")
    return {
        "source_sha": commit,
        "tag": tag,
        "version": version,
        "source_archive_sha256": file_sha256(archive),
        "dependency_lock_sha256": file_sha256(lockfile),
        "artifact_format": "git-archive-tar-gzip-no-timestamp",
    }


def verify_bundle_manifest(
    *, manifest: dict[str, Any], archive: Path,
    project_file: Path, lockfile: Path,
    tag: str, commit: str,
) -> None:
    expected = create_bundle_manifest(
        archive=archive, project_file=project_file,
        lockfile=lockfile, tag=tag, commit=commit,
    )
    if manifest != expected:
        raise ValueError("release archive/lockfile checksum or source mismatch")


def main() -> int:
    parser = argparse.ArgumentParser(description="Release verification gates")
    actions = parser.add_subparsers(dest="action", required=True)
    source = actions.add_parser("verify-source")
    source.add_argument("--tag", required=True)
    source.add_argument("--sha", required=True)
    source.add_argument("--check-main", action="store_true")
    source.add_argument("--check-tag-ref", action="store_true")

    create = actions.add_parser("create-manifest")
    create.add_argument("--tag", required=True)
    create.add_argument("--sha", required=True)
    create.add_argument("--archive", required=True, type=Path)
    create.add_argument("--output", required=True, type=Path)

    verify = actions.add_parser("verify-manifest")
    verify.add_argument("--tag", required=True)
    verify.add_argument("--sha", required=True)
    verify.add_argument("--archive", required=True, type=Path)
    verify.add_argument("--manifest", required=True, type=Path)

    preflight = actions.add_parser("preflight")
    preflight.add_argument("--plan", required=True, type=Path)

    args = parser.parse_args()
    try:
        if args.action == "verify-source":
            verify_source_commit(
                tag=args.tag, commit=args.sha,
                pyproject=Path("pyproject.toml"),
                check_main=args.check_main,
                check_tag_ref=args.check_tag_ref,
            )
            print('{"source_verified": true}')
            return 0
        if args.action == "preflight":
            with args.plan.open(encoding="utf-8") as stream:
                record = json.load(stream)
            decision = ReleaseReadinessEvaluator().evaluate(record)
            print(json.dumps(decision.to_dict(), sort_keys=True))
            return 0 if decision.allowed else 1

        if args.action == "create-manifest":
            record = create_bundle_manifest(
                archive=args.archive, project_file=Path("pyproject.toml"),
                lockfile=Path("uv.lock"), tag=args.tag, commit=args.sha,
            )
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(
                json.dumps(record, sort_keys=True, indent=2) + "\n",
                encoding="utf-8",
            )
            print('{"manifest_created": true}')
            return 0
        if args.action == "verify-manifest":
            with args.manifest.open(encoding="utf-8") as stream:
                record = json.load(stream)
            verify_bundle_manifest(
                manifest=record, archive=args.archive,
                project_file=Path("pyproject.toml"),
                lockfile=Path("uv.lock"), tag=args.tag, commit=args.sha,
            )
            print('{"artifact_verified": true}')
            return 0
    except (KeyError, OSError, ValueError, TypeError, tarfile.TarError,
            subprocess.SubprocessError, json.JSONDecodeError):
        print('{"verified": false, "reason": "invalid release evidence"}')
        return 2
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
