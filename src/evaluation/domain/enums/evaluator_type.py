from __future__ import annotations

from enum import Enum


class EvaluatorType(str, Enum):
    """
    Skorlayıcının tipini temsil eder.
    """

    HUMAN = "HUMAN"
    LLM = "LLM"