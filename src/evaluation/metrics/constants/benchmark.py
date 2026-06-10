from __future__ import annotations

from typing import Final


STRONG_BENCHMARK_THRESHOLD: Final[float] = 0.80
MODERATE_BENCHMARK_THRESHOLD: Final[float] = 0.60

ALIGNMENT_WEIGHT: Final[float] = 0.60
CATEGORY_WEIGHT: Final[float] = 0.40

STRONG_BENCHMARK_INTERPRETATION: Final[str] = "strong_benchmark"
MODERATE_BENCHMARK_INTERPRETATION: Final[str] = "moderate_benchmark"
WEAK_BENCHMARK_INTERPRETATION: Final[str] = "weak_benchmark"