from __future__ import annotations

from typing import Final


SEMANTIC_SCORE_WEIGHT: Final[float] = 0.60
MARKET_SCORE_WEIGHT: Final[float] = 0.20
DIFFICULTY_SCORE_WEIGHT: Final[float] = 0.10
DIVERSITY_SCORE_WEIGHT: Final[float] = 0.10

DEFAULT_LEVEL_SCORE: Final[float] = 0.0
DEFAULT_CV_GAP_SCORE: Final[float] = 0.0
DEFAULT_FATIGUE_SCORE: Final[float] = 0.0
DEFAULT_DIVERSITY_SCORE: Final[float] = 1.0

MIN_NORMALIZED_SCORE: Final[float] = 0.0
MAX_NORMALIZED_SCORE: Final[float] = 1.0

NORMALIZED_SCORE_BASE: Final[float] = 1.0

DIFFICULTY_DISTANCE_NORMALIZER: Final[float] = 10.0