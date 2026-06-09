from __future__ import annotations

from typing import Final


DEFAULT_ALPHA: Final[float] = 0.05

PAIRED_T_TEST_NAME: Final[str] = "paired_t_test"

MIN_PAIRED_T_TEST_SAMPLE_COUNT: Final[int] = 2

MIN_P_VALUE: Final[float] = 0.0
MAX_P_VALUE: Final[float] = 1.0

MIN_ALPHA: Final[float] = 0.0
MAX_ALPHA: Final[float] = 1.0

ZERO_STANDARD_DEVIATION_THRESHOLD: Final[float] = 1e-12