"""Search filter rules as typed ValidationRule objects, not dictionaries."""

from __future__ import annotations

from typing import Final

from src.domain.enums.question_category import QuestionCategory
from src.domain.enums.question_type import QuestionType
from src.domain.enums.level import Level
from src.domain.validation.schema_rules import ValidationRule
from src.domain.validation.schema_types import ValidationSchema

_OPTIONAL_DIFFICULTY = ValidationRule(
    expected_type=(int, float),
    nullable=True,
    reject_bool=True,
    finite=True,
    min_value=0,
    max_value=10,
)

SEARCH_FILTERS_SCHEMA: Final[ValidationSchema] = {
    "category": ValidationRule(expected_type=QuestionCategory, nullable=True),
    "level": ValidationRule(expected_type=Level, nullable=True),
    "question_type": ValidationRule(expected_type=QuestionType, nullable=True),
    "min_difficulty": _OPTIONAL_DIFFICULTY,
    "max_difficulty": _OPTIONAL_DIFFICULTY,
}
