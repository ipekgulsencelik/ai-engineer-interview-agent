from __future__ import annotations

from enum import StrEnum
from typing import TypeVar

EnumT = TypeVar(
    "EnumT",
    bound=StrEnum,
)


class EnumParserValidator:
    """
    Raw enum parser input validator.
    """

    @staticmethod
    def validate_raw_enum_input(
        *,
        value: object,
        enum_class: type[EnumT],
        field_name: str,
    ) -> None:
        if isinstance(value, bool):
            raise TypeError(
                f"{field_name} must be {enum_class.__name__} or string."
            )

        if isinstance(value, enum_class):
            return

        if not isinstance(value, str):
            raise TypeError(
                f"{field_name} must be {enum_class.__name__} or string."
            )

        if not value.strip():
            raise ValueError(
                f"{field_name} cannot be empty."
            )