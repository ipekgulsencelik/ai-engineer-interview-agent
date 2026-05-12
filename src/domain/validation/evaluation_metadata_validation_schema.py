from __future__ import annotations

from typing import Any

from src.domain.constants.evaluation import (
    DEFAULT_RUBRIC_VERSION,
    MAX_CONFIDENCE_SCORE,
    MIN_CONFIDENCE_SCORE,
)


NUMBER_TYPES = (int, float)


EVALUATION_METADATA_VALIDATION_SCHEMA: dict[str, dict[str, Any]] = {
    "confidence": {
        "type": NUMBER_TYPES,
        "finite": True,
        "min_value": MIN_CONFIDENCE_SCORE,
        "max_value": MAX_CONFIDENCE_SCORE,
    },
    "latency_seconds": {
        "type": NUMBER_TYPES,
        "nullable": True,
        "finite": True,
        "min_value": 0.0,
    },
    "rubric_version": {
        "type": str,
        "non_empty": True,
        "default": DEFAULT_RUBRIC_VERSION,
    },
    "missing_keywords": {
        "type": tuple,
        "item_type": str,
    },
    "follow_up_question": {
        "type": str,
        "nullable": True,
        "non_empty": True,
    },
}