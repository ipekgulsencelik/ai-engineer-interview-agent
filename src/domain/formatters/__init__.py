from __future__ import annotations

from enum import StrEnum
from typing import TypeVar

EnumT = TypeVar(
    "EnumT",
    bound=StrEnum,
)


class EnumErrorMessageBuilder:
    """
    Enum parsing error message builder.
    """

    @staticmethod
    def build_invalid_enum_error(
        *,
        field_name: str,
        value: object,
        enum_class: type[EnumT],
    ) -> str:
        allowed_values = ", ".join(
            item.value
            for item in enum_class
        )

        return (
            f"Invalid {field_name}: {value}. "
            f"Expected one of: "
            f"{allowed_values}."
        )