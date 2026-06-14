from __future__ import annotations

from enum import Enum


class HallucinationLabel(
    str,
    Enum,
):
    """
    Hallucination taxonomy labels.
    """

    NONE = "none"

    LOW = "low"

    MEDIUM = "medium"

    HIGH = "high"

    CRITICAL = "critical"

    SUPPORTED = "supported"

    UNSUPPORTED = "unsupported"

    CONTRADICTED = "contradicted"

    FABRICATED = "fabricated"