from __future__ import annotations

from typing import Final


STRONG_ALIGNMENT_THRESHOLD: Final[float] = 0.80
MODERATE_ALIGNMENT_THRESHOLD: Final[float] = 0.60

MIN_ALIGNMENT_SCORE: Final[float] = 0.0
MAX_ALIGNMENT_SCORE: Final[float] = 1.0

ALIGNMENT_METRIC_COUNT: Final[int] = 3

HUMAN_SCORE_METRIC_NAME: Final[str] = "human_score"
LLM_SCORE_METRIC_NAME: Final[str] = "llm_score"

HUMAN_LLM_AGREEMENT_METRIC_NAME: Final[str] = "human_llm_agreement"
HUMAN_LLM_REGRESSION_METRIC_NAME: Final[str] = "human_llm_regression"

STRONG_ALIGNMENT_INTERPRETATION: Final[str] = "strong_alignment"
MODERATE_ALIGNMENT_INTERPRETATION: Final[str] = "moderate_alignment"
WEAK_ALIGNMENT_INTERPRETATION: Final[str] = "weak_alignment"