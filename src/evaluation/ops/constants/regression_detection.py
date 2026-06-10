from __future__ import annotations

from typing import Final


DEFAULT_REGRESSION_THRESHOLD: Final[float] = 0.03

REGRESSION_DETECTED_INTERPRETATION: Final[str] = "regression_detected"
NO_REGRESSION_INTERPRETATION: Final[str] = "no_regression"
IMPROVEMENT_DETECTED_INTERPRETATION: Final[str] = "improvement_detected"