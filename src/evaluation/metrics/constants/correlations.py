from __future__ import annotations

from typing import Final


MIN_CORRELATION_SAMPLE_COUNT: Final[int] = 2

CORRELATION_MIN_VALUE: Final[float] = -1.0
CORRELATION_MAX_VALUE: Final[float] = 1.0

P_VALUE_MIN: Final[float] = 0.0
P_VALUE_MAX: Final[float] = 1.0

DEFAULT_SIGNIFICANCE_LEVEL: Final[float] = 0.05

ZERO_DENOMINATOR_THRESHOLD: Final[float] = 1e-12

PEARSON_METHOD_NAME: Final[str] = "pearson"

VERY_STRONG_CORRELATION_THRESHOLD: Final[float] = 0.90
STRONG_CORRELATION_THRESHOLD: Final[float] = 0.70
MODERATE_CORRELATION_THRESHOLD: Final[float] = 0.50
WEAK_CORRELATION_THRESHOLD: Final[float] = 0.30