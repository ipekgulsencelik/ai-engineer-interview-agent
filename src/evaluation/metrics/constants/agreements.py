from __future__ import annotations

from typing import Final


MIN_AGREEMENT_SAMPLE_COUNT: Final[int] = 1

AGREEMENT_MIN_RATIO: Final[float] = 0.0
AGREEMENT_MAX_RATIO: Final[float] = 1.0

DEFAULT_AGREEMENT_RELIABILITY_THRESHOLD: Final[float] = 0.70

COHEN_KAPPA_METHOD_NAME: Final[str] = "cohen_kappa"

KAPPA_ZERO_DENOMINATOR_THRESHOLD: Final[float] = 1e-12

VERY_STRONG_AGREEMENT_THRESHOLD: Final[float] = 0.90
STRONG_AGREEMENT_THRESHOLD: Final[float] = 0.70
MODERATE_AGREEMENT_THRESHOLD: Final[float] = 0.50
WEAK_AGREEMENT_THRESHOLD: Final[float] = 0.30

FLEISS_KAPPA_METHOD_NAME: Final[str] = "fleiss_kappa"

MIN_FLEISS_EVALUATOR_COUNT: Final[int] = 2