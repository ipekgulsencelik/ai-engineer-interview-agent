"""Allow only reviewed, immutable Python 3.11 Trixie release-image references.

The policy checks identity syntax. It does not attest, retrieve, sign or approve
a digest; operations must independently verify and record the chosen digest.
"""

from __future__ import annotations

import re


class ApprovedPythonBaseImagePolicy:
    """Fail-closed input validation for the production release image ref."""

    _PATTERN = re.compile(
        r"docker\.io/library/python:3\.11-slim-trixie@sha256:[a-f0-9]{64}\Z"
    )

    @classmethod
    def validate(cls, image: object) -> str:
        if not isinstance(image, str) or cls._PATTERN.fullmatch(image) is None:
            raise ValueError(
                "An approved immutable Docker Hub Python 3.11 "
                "Trixie SHA-256 image reference is required."
            )
        return image
