from __future__ import annotations

from typing import Any


NUMBER_TYPES = (int, float)


SCORING_WEIGHTS_VALIDATION_SCHEMA: dict[str, dict[str, Any]] = {
    "level_weight": {
        "type": NUMBER_TYPES,
        "finite": True,
        "min_value": 0.0,
    },
    "market_weight": {
        "type": NUMBER_TYPES,
        "finite": True,
        "min_value": 0.0,
    },
    "cv_gap_weight": {
        "type": NUMBER_TYPES,
        "finite": True,
        "min_value": 0.0,
    },
    "difficulty_weight": {
        "type": NUMBER_TYPES,
        "finite": True,
        "min_value": 0.0,
    },
    "diversity_weight": {
        "type": NUMBER_TYPES,
        "finite": True,
        "min_value": 0.0,
    },
    "fatigue_weight": {
        "type": NUMBER_TYPES,
        "finite": True,
        "min_value": 0.0,
    },
    "semantic_relevance_weight": {
        "type": NUMBER_TYPES,
        "finite": True,
        "min_value": 0.0,
    },
}