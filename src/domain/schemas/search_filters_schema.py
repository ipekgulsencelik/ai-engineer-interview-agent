from __future__ import annotations

from typing import Final

from src.domain.enums.category import Category
from src.domain.enums.level import Level
from src.domain.validation.schema_types import (
    ValidationSchema,
)
from src.domain.validation.validation_rules import (
    OPTIONAL_NON_EMPTY_STRING_RULE,
)


SEARCH_FILTERS_SCHEMA: Final[ValidationSchema] = {
    "category": {
        "type": Category,
        "nullable": True,
    },
    "level": {
        "type": Level,
        "nullable": True,
    },
    "question_type": {
        "type": str,
        "nullable": True,
        "non_empty": True,
        "strip": True,
    },
    "min_difficulty": {
        "type": (int, float),
        "nullable": True,
        "reject_bool": True,
        "min_value": 0,
        "max_value": 10,
    },
    "max_difficulty": {
        "type": (int, float),
        "nullable": True,
        "reject_bool": True,
        "min_value": 0,
        "max_value": 10,
    },
    "keyword": OPTIONAL_NON_EMPTY_STRING_RULE,
}