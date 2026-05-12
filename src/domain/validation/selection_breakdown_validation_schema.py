from __future__ import annotations

from typing import Any

from src.domain.constants.selection import (
    MAX_NORMALIZED_SCORE,
    MIN_FINAL_SCORE,
    MIN_NORMALIZED_SCORE,
)


NUMBER_TYPES = (int, float)

SELECTION_BREAKDOWN_VALIDATION_SCHEMA: dict[str, dict[str, Any]] = {
    "level_score": {
        "type": NUMBER_TYPES,
        "finite": True,
        "min_value": MIN_NORMALIZED_SCORE,
        "max_value": MAX_NORMALIZED_SCORE,
    },
    "market_score": {
        "type": NUMBER_TYPES,
        "finite": True,
        "min_value": MIN_NORMALIZED_SCORE,
        "max_value": MAX_NORMALIZED_SCORE,
    },
    "cv_gap_score": {
        "type": NUMBER_TYPES,
        "finite": True,
        "min_value": MIN_NORMALIZED_SCORE,
        "max_value": MAX_NORMALIZED_SCORE,
    },
    "difficulty_score": {
        "type": NUMBER_TYPES,
        "finite": True,
        "min_value": MIN_NORMALIZED_SCORE,
        "max_value": MAX_NORMALIZED_SCORE,
    },
    "diversity_score": {
        "type": NUMBER_TYPES,
        "finite": True,
        "min_value": MIN_NORMALIZED_SCORE,
        "max_value": MAX_NORMALIZED_SCORE,
    },
    "fatigue_score": {
        "type": NUMBER_TYPES,
        "finite": True,
        "min_value": MIN_NORMALIZED_SCORE,
        "max_value": MAX_NORMALIZED_SCORE,
    },
    "final_score": {
        "type": NUMBER_TYPES,
        "finite": True,
        "min_value": MIN_FINAL_SCORE,
    },
}