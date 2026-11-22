"""Fail closed when a required live integration job skips tests."""

from __future__ import annotations

import argparse
from pathlib import Path

from src.application.quality.integration_test_coverage import (
    summarize_integration_junit,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Require real integration tests to execute without skips."
    )
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args(argv)

    try:
        report = args.report.read_text(encoding="utf-8")
        result = summarize_integration_junit(report)
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"Integration test evidence invalid: {type(exc).__name__}")
        return 1

    print(
        f"Required integration: collected={result.collected}, "
        f"skipped={result.skipped}, failures={result.failures}, "
        f"errors={result.errors}"
    )
    if not result.valid:
        print("FAIL: required live integrations must run with zero skips.")
        return 1
    print("PASS: all required live integration cases executed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
