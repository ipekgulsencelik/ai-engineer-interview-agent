"""Release must not build from mutable or unreviewed Python base identities."""

from __future__ import annotations

import pytest

from src.application.release.approved_python_base_image_policy import (
    ApprovedPythonBaseImagePolicy,
)
from src.infrastructure.operations.verify_release_base_image import main


_APPROVED = "docker.io/library/python:3.11-slim-trixie@sha256:" + "a" * 64


def test_accepts_reviewed_digest_reference_format() -> None:
    assert ApprovedPythonBaseImagePolicy.validate(_APPROVED) == _APPROVED


@pytest.mark.parametrize(
    "image",
    [
        None,
        "",
        "python:3.11-slim",
        "python:3.11-slim-trixie",
        "docker.io/library/python:latest@sha256:" + "a" * 64,
        "docker.io/library/python:3.13-slim-trixie@sha256:" + "a" * 64,
        "docker.io/library/python:3.11-slim-bookworm@sha256:" + "a" * 64,
        "evil.example/python:3.11-slim-trixie@sha256:" + "a" * 64,
        "docker.io/library/python:3.11-slim-trixie@sha256:" + "g" * 64,
        _APPROVED + "\n",
        42,
    ],
)
def test_rejects_mutable_unknown_and_malformed_image_refs(image: object) -> None:
    with pytest.raises(ValueError, match="immutable"):
        ApprovedPythonBaseImagePolicy.validate(image)


def test_cli_defaults_to_release_block(monkeypatch, capsys) -> None:
    monkeypatch.delenv("APPROVED_PYTHON_BASE_IMAGE", raising=False)
    assert main() == 1
    result = capsys.readouterr()
    assert "Release blocked" in result.err


def test_cli_does_not_leak_supplied_malformed_image(monkeypatch, capsys) -> None:
    secret = "private-image-with-secret-token"
    monkeypatch.setenv("APPROVED_PYTHON_BASE_IMAGE", secret)
    assert main() == 1
    result = capsys.readouterr()
    assert secret not in result.out + result.err


def test_cli_can_validate_explicit_digest(monkeypatch) -> None:
    monkeypatch.setenv("APPROVED_PYTHON_BASE_IMAGE", _APPROVED)
    assert main() == 0
