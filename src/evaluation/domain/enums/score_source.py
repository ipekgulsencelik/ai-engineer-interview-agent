from __future__ import annotations

from enum import Enum


class ScoreSource(str, Enum):
    """
    Skorun hangi kaynaktan geldiğini temsil eder.
    """

    HUMAN_EXPERT = "HUMAN_EXPERT"
    GROQ_LLM = "GROQ_LLM"
    BASELINE_MODEL = "BASELINE_MODEL"