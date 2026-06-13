from __future__ import annotations

from typing import Final

from src.domain.validation.schema_rules import (
    ValidationRule,
)


NON_EMPTY_STRING_RULE: Final[ValidationRule] = ValidationRule(
    expected_type=str,
    non_empty=True,
    strip=True,
)

OPTIONAL_NON_EMPTY_STRING_RULE: Final[ValidationRule] = ValidationRule(
    expected_type=str,
    nullable=True,
    non_empty=True,
    strip=True,
)

STRING_RULE: Final[ValidationRule] = ValidationRule(
    expected_type=str,
)

OPTIONAL_STRING_RULE: Final[ValidationRule] = ValidationRule(
    expected_type=str,
    nullable=True,
)

BOOLEAN_RULE: Final[ValidationRule] = ValidationRule(
    expected_type=bool,
)

OPTIONAL_BOOLEAN_RULE: Final[ValidationRule] = ValidationRule(
    expected_type=bool,
    nullable=True,
)

NUMBER_RULE: Final[ValidationRule] = ValidationRule(
    expected_type=(int, float),
    reject_bool=True,
    finite=True,
)

OPTIONAL_NUMBER_RULE: Final[ValidationRule] = ValidationRule(
    expected_type=(int, float),
    nullable=True,
    reject_bool=True,
    finite=True,
)

NON_NEGATIVE_NUMBER_RULE: Final[ValidationRule] = ValidationRule(
    expected_type=(int, float),
    reject_bool=True,
    finite=True,
    min_value=0,
)

PERCENTAGE_RULE: Final[ValidationRule] = ValidationRule(
    expected_type=(int, float),
    reject_bool=True,
    finite=True,
    min_value=0,
    max_value=100,
)

DICT_RULE: Final[ValidationRule] = ValidationRule(
    expected_type=dict,
)

OPTIONAL_DICT_RULE: Final[ValidationRule] = ValidationRule(
    expected_type=dict,
    nullable=True,
)

METADATA_RULE: Final[ValidationRule] = ValidationRule(
    expected_type=dict,
    allow_empty=True,
)

OPTIONAL_METADATA_RULE: Final[ValidationRule] = ValidationRule(
    expected_type=dict,
    nullable=True,
    allow_empty=True,
)

STRING_TUPLE_RULE: Final[ValidationRule] = ValidationRule(
    expected_type=tuple,
    item_type=str,
    allow_empty=True,
    strip_items=True,
)

OPTIONAL_STRING_TUPLE_RULE: Final[ValidationRule] = ValidationRule(
    expected_type=tuple,
    nullable=True,
    item_type=str,
    allow_empty=True,
    strip_items=True,
)

LIST_STRING_RULE: Final[ValidationRule] = ValidationRule(
    expected_type=list,
    item_type=str,
)

OPTIONAL_LIST_STRING_RULE: Final[ValidationRule] = ValidationRule(
    expected_type=list,
    nullable=True,
    item_type=str,
)

NON_EMPTY_LIST_STRING_RULE: Final[ValidationRule] = ValidationRule(
    expected_type=list,
    item_type=str,
    non_empty=True,
)

DATETIME_RULE: Final[ValidationRule] = ValidationRule(
    expected_type=str,
    non_empty=True,
    strip=True,
)

SEMVER_RULE: Final[ValidationRule] = ValidationRule(
    expected_type=str,
    non_empty=True,
    strip=True,
)

CORRELATION_RULE: Final[ValidationRule] = ValidationRule(
    expected_type=(int, float),
    reject_bool=True,
    finite=True,
    min_value=-1,
    max_value=1,
)

NON_NEGATIVE_FLOAT_RULE: Final[ValidationRule] = ValidationRule(
    expected_type=(int, float),
    reject_bool=True,
    finite=True,
    min_value=0,
)

POSITIVE_INTEGER_RULE: Final[ValidationRule] = ValidationRule(
    expected_type=int,
    reject_bool=True,
    finite=True,
    min_value=1,
)

NON_NEGATIVE_INTEGER_RULE: Final[ValidationRule] = ValidationRule(
    expected_type=int,
    reject_bool=True,
    finite=True,
    min_value=0,
)

OPTIONAL_INTEGER_RULE: Final[ValidationRule] = ValidationRule(
    expected_type=int,
    nullable=True,
    reject_bool=True,
    finite=True,
)

RATIO_RULE: Final[ValidationRule] = ValidationRule(
    expected_type=(int, float),
    reject_bool=True,
    finite=True,
    min_value=0,
    max_value=1,
)

OPTIONAL_RATIO_RULE: Final[ValidationRule] = ValidationRule(
    expected_type=(int, float),
    nullable=True,
    reject_bool=True,
    finite=True,
    min_value=0,
    max_value=1,
)

P_VALUE_RULE: Final[ValidationRule] = ValidationRule(
    expected_type=(int, float),
    nullable=True,
    reject_bool=True,
    finite=True,
    min_value=0,
    max_value=1,
)

R2_SCORE_RULE: Final[ValidationRule] = ValidationRule(
    expected_type=(int, float),
    reject_bool=True,
    finite=True,
    min_value=-1,
    max_value=1,
)
