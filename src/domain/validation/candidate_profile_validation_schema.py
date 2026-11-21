"""Validation schema for the provider-neutral candidate profile aggregate."""

from __future__ import annotations

from typing import Final

from src.domain.enums.level import Level
from src.domain.validation.common_rules import (
    NON_NEGATIVE_NUMBER_RULE,
    OPTIONAL_NON_EMPTY_STRING_RULE,
    STRING_TUPLE_RULE,
)
from src.domain.validation.schema_rules import ValidationRule
from src.domain.validation.schema_types import ValidationSchema

CANDIDATE_PROFILE_SCHEMA: Final[ValidationSchema] = {
    "detected_level": ValidationRule(expected_type=Level),
    "years_of_experience": NON_NEGATIVE_NUMBER_RULE,
    "skills": STRING_TUPLE_RULE,
    "weak_skills": STRING_TUPLE_RULE,
    "target_roles": STRING_TUPLE_RULE,
    "education": STRING_TUPLE_RULE,
    "projects": STRING_TUPLE_RULE,
    "summary": OPTIONAL_NON_EMPTY_STRING_RULE,
}
