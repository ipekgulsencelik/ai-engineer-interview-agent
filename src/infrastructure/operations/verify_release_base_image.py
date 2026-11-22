"""Fail closed if the release workflow has no approved immutable base."""

from __future__ import annotations

import os
import sys

from src.application.release.approved_python_base_image_policy import (
    ApprovedPythonBaseImagePolicy,
)


def main() -> int:
    try:
        ApprovedPythonBaseImagePolicy.validate(
            os.environ.get("APPROVED_PYTHON_BASE_IMAGE")
        )
    except ValueError:
        # Do not echo environment values into public CI logs.
        print("Release blocked: approved immutable Python image required.", file=sys.stderr)
        return 1
    print("Python base-image digest reference format verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
