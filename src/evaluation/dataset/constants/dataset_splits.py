from __future__ import annotations

from typing import Final


DEFAULT_TRAIN_RATIO: Final[float] = 0.70
DEFAULT_VALIDATION_RATIO: Final[float] = 0.20
DEFAULT_TEST_RATIO: Final[float] = 0.10

DEFAULT_SPLIT_SEED: Final[int] = 42

MIN_SPLITTABLE_SAMPLE_COUNT: Final[int] = 3

SPLIT_RATIO_SUM_TARGET: Final[float] = 1.0
SPLIT_RATIO_TOLERANCE: Final[float] = 1e-9