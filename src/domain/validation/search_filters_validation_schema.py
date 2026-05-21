from __future__ import annotations

from typing import Any, Final

from src.domain.constants.question import (
    MAX_DIFFICULTY,
    MIN_DIFFICULTY,
)
from src.domain.enums.level import Level
from src.domain.enums.question_category import (
    QuestionCategory,
)
from src.domain.enums.question_type import (
    QuestionType,
)


SEARCH_FILTERS_VALIDATION_SCHEMA: Final[
    dict[str, dict[str, Any]]
] = {
    "category": {
        "type": QuestionCategory,
        "nullable": True,
    },
    "level": {
        "type": Level,
        "nullable": True,
    },
    "question_type": {
        "type": QuestionType,
        "nullable": True,
    },
    "min_difficulty": {
        "type": int,
        "nullable": True,
        "reject_bool": True,
        "min_value": MIN_DIFFICULTY,
        "max_value": MAX_DIFFICULTY,
    },
    "max_difficulty": {
        "type": int,
        "nullable": True,
        "reject_bool": True,
        "min_value": MIN_DIFFICULTY,
        "max_value": MAX_DIFFICULTY,
    },
}