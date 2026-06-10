from __future__ import annotations

from typing import Final

from src.domain.entities.question import Question
from src.domain.validation.schema_types import ValidationSchema


SEARCH_RESULT_VALIDATION_SCHEMA: Final[ValidationSchema] = {
    "question": {
        "type": Question,
        "nullable": False,
    },
    "distance": {
        "type": (int, float),
        "finite": True,
        "reject_bool": True,
        "min_value": 0.0,
        "nullable": False,
    },
    "score": {
        "type": (int, float),
        "finite": True,
        "reject_bool": True,
        "min_value": 0.0,
        "max_value": 1.0,
        "nullable": False,
    },
}
