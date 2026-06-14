from __future__ import annotations

from enum import Enum


class HallucinationLabel(
    str,
    Enum,
):
    """
    Hallucination taxonomy labels.
    """

    SUPPORTED = "supported"

    UNSUPPORTED = "unsupported"

    CONTRADICTED = "contradicted"

    FABRICATED = "fabricated"