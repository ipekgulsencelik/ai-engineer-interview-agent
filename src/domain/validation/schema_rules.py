from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ValidationRule:
    """
    Immutable field validation definition.

    Validation schema içerisinde her field için
    uygulanacak kuralları tanımlar.
    """

    expected_type: type | tuple[type, ...]

    nullable: bool = False

    non_empty: bool = False
    strip: bool = False

    allow_empty: bool = True

    item_type: type | tuple[type, ...] | None = None
    strip_items: bool = False

    reject_bool: bool = False
    finite: bool = False

    min_value: int | float | None = None
    max_value: int | float | None = None

    min_length: int | None = None
    max_length: int | None = None

    allowed_values: frozenset[Any] | None = None