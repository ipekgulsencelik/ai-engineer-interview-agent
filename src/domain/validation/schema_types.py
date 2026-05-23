from __future__ import annotations

from typing import Any, TypeAlias, TypedDict


class ValidationRule(TypedDict, total=False):
    """
    Schema-driven validation rule contract.
    """

    type: type | tuple[type, ...]
    item_type: type | tuple[type, ...]
    key_type: type | tuple[type, ...]
    value_type: type | tuple[type, ...]

    nullable: bool
    non_empty: bool
    non_empty_items: bool
    strip: bool

    finite: bool
    finite_items: bool

    reject_bool: bool
    reject_bool_items: bool
    reject_bool_values: bool

    min_value: int | float
    max_value: int | float
    min_item_value: int | float
    max_item_value: int | float

    non_negative: bool
    timezone_aware: bool

    default: Any


ValidationSchema: TypeAlias = dict[str, ValidationRule]
