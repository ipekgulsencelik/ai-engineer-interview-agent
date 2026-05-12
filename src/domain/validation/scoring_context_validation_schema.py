from __future__ import annotations

from typing import Any

from src.domain.enums.level import Level
from src.domain.scoring.scoring_signals import ScoringSignals


NUMBER_TYPES = (int, float)


SCORING_CONTEXT_VALIDATION_SCHEMA: dict[str, dict[str, Any]] = {
    "current_level": {
        "type": Level,
    },
    "cv_skills": {
        "type": tuple,
        "item_type": str,
    },
    "asked_question_ids": {
        "type": frozenset,
        "item_type": str,
    },
    "recent_scores": {
        "type": tuple,
        "item_type": NUMBER_TYPES,
        "finite_items": True,
        "min_item_value": 0.0,
        "max_item_value": 10.0,
    },
    "weak_areas": {
        "type": tuple,
        "item_type": str,
    },
    "signals": {
        "type": ScoringSignals,
    },
}