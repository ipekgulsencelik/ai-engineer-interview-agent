from __future__ import annotations

from typing import Any
from typing import Final

from src.domain.constants.scoring import (
    MAX_NORMALIZED_SCORE,
    MIN_NORMALIZED_SCORE,
)


NORMALIZED_SCORE_RULE: Final[dict[str, Any]] = {
    "type": (int, float),
    "finite": True,
    "reject_bool": True,
    "min_value": MIN_NORMALIZED_SCORE,
    "max_value": MAX_NORMALIZED_SCORE,
}


SELECTION_BREAKDOWN_VALIDATION_SCHEMA: Final[
    dict[str, dict[str, Any]]
] = {
    "level_score": NORMALIZED_SCORE_RULE,
    "semantic_score": NORMALIZED_SCORE_RULE,
    "market_score": NORMALIZED_SCORE_RULE,
    "cv_gap_score": NORMALIZED_SCORE_RULE,
    "difficulty_score": NORMALIZED_SCORE_RULE,
    "diversity_score": NORMALIZED_SCORE_RULE,
    "fatigue_score": NORMALIZED_SCORE_RULE,
    "final_score": {
        "type": (int, float),
        "finite": True,
        "reject_bool": True,
        "min_value": 0.0,
    },
}