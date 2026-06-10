from __future__ import annotations

from enum import Enum


class AgreementLevel(str, Enum):
    """
    Human-LLM agreement classification levels.
    """

    VERY_LOW = "very_low"
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    VERY_HIGH = "very_high"