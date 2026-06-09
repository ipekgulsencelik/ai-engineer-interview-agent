from __future__ import annotations

from typing import Final


MIN_REGRESSION_SAMPLE_COUNT: Final[int] = 1

MIN_REGRESSION_ERROR: Final[float] = 0.0

MIN_R2_SCORE: Final[float] = -1.0
MAX_R2_SCORE: Final[float] = 1.0

ZERO_TOTAL_VARIANCE_THRESHOLD: Final[float] = 1e-12

EXCELLENT_R2_THRESHOLD: Final[float] = 0.90
GOOD_R2_THRESHOLD: Final[float] = 0.75
MODERATE_R2_THRESHOLD: Final[float] = 0.50

DEFAULT_ACCEPTABLE_R2_THRESHOLD: Final[float] = 0.70