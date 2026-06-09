from __future__ import annotations

from typing import Final


VERY_STRONG_CORRELATION_THRESHOLD: Final = 0.90
STRONG_CORRELATION_THRESHOLD: Final = 0.70
MODERATE_CORRELATION_THRESHOLD: Final = 0.50
WEAK_CORRELATION_THRESHOLD: Final = 0.30


ALMOST_PERFECT_KAPPA_THRESHOLD: Final = 0.81
STRONG_KAPPA_THRESHOLD: Final = 0.61
MODERATE_KAPPA_THRESHOLD: Final = 0.41
FAIR_KAPPA_THRESHOLD: Final = 0.21


# ============================================================
# Regression Thresholds
# ============================================================

EXCELLENT_MAE_THRESHOLD: Final[float] = 0.25
GOOD_MAE_THRESHOLD: Final[float] = 0.50
MODERATE_MAE_THRESHOLD: Final[float] = 1.00


# ============================================================
# Statistical Significance
# ============================================================

DEFAULT_SIGNIFICANCE_LEVEL: Final[float] = 0.05


# ============================================================
# Alignment Thresholds
# ============================================================

STRONG_ALIGNMENT_THRESHOLD: Final[float] = 0.80
MODERATE_ALIGNMENT_THRESHOLD: Final[float] = 0.60


# ============================================================
# Benchmark Thresholds
# ============================================================

STRONG_BENCHMARK_THRESHOLD: Final[float] = 0.80

MODERATE_BENCHMARK_THRESHOLD: Final[float] = 0.60


# ============================================================
# Reliability Thresholds
# ============================================================

DEFAULT_AGREEMENT_RELIABILITY_THRESHOLD: Final[
    float
] = 0.60

DEFAULT_MODEL_ALIGNMENT_THRESHOLD: Final[
    float
] = 0.70


# ============================================================
# Correlation Validation
# ============================================================

MIN_CORRELATION_SAMPLE_COUNT: Final[int] = 2


# ============================================================
# Generic Score Bounds
# ============================================================

MIN_SCORE: Final[float] = 0.0

MAX_SCORE: Final[float] = 1.0