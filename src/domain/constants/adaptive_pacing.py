from __future__ import annotations

from typing import Final


DEFAULT_DIFFICULTY_MULTIPLIER: Final[float] = 1.0

INCREASE_DIFFICULTY_MULTIPLIER: Final[float] = 1.15

REDUCE_DIFFICULTY_MULTIPLIER: Final[float] = 0.85

INCREASE_SCORE_THRESHOLD: Final[float] = 8.0

REDUCE_SCORE_THRESHOLD: Final[float] = 4.0

DIFFICULTY_STEP: Final[int] = 1

MIN_TARGET_DIFFICULTY: Final[int] = 1
MAX_TARGET_DIFFICULTY: Final[int] = 10

MIN_DIFFICULTY_MULTIPLIER: Final[float] = 0.0