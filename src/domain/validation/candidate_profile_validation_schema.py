from __future__ import annotations

from typing import Final

from src.domain.enums.level import Level
from src.domain.validation.schema_types import (
    ValidationRule,
    ValidationSchema,
)
from src.domain.validation.validation_rules import (
    FINITE_NUMBER_RULE,
    OPTIONAL_NON_EMPTY_STRING_RULE,
)


STRING_TUPLE_RULE: Final[ValidationRule] = {
    "type": tuple,
    "nullable": False,
    "item_type": str,
}


CANDIDATE_PROFILE_SCHEMA: Final[ValidationSchema] = {
    "detected_level": {
        "type": Level,
        "nullable": False,
    },
    "years_of_experience": {
        **FINITE_NUMBER_RULE,
        "min_value": 0,
    },
    "skills": STRING_TUPLE_RULE,
    "weak_skills": STRING_TUPLE_RULE,
    "target_roles": STRING_TUPLE_RULE,
    "education": STRING_TUPLE_RULE,
    "projects": STRING_TUPLE_RULE,
    "summary": OPTIONAL_NON_EMPTY_STRING_RULE,
}