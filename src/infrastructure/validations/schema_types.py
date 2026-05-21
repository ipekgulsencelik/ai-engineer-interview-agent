from __future__ import annotations

from typing import Any, TypeAlias, TypedDict


ValidationType: TypeAlias = Any


class SchemaRule(TypedDict, total=False):
    type: ValidationType
    non_empty: bool
    strip: bool
    allow_empty: bool
    item_type: ValidationType
    strip_items: bool
    min_value: float | int
    max_value: float | int
    allow_bool: bool


SchemaDefinition: TypeAlias = dict[str, SchemaRule]