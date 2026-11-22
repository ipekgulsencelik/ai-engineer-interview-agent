"""Regression: Git Bash receives only LF bytes through Python subprocess."""

from __future__ import annotations

import subprocess


def test_bash_syntax_validation_accepts_normalized_windows_crlf() -> None:
    script_with_crlf = (
        b"#!/usr/bin/env bash\r\n"
        b"for executable in docker mktemp; do\r\n"
        b"  :\r\n"
        b"done\r\n"
    )
    normalized = script_with_crlf.replace(b"\r\n", b"\n")
    assert b"\r" not in normalized
    result = subprocess.run(
        ["bash", "-n", "-"],
        input=normalized,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr.decode(
        "utf-8", errors="replace"
    )
