from __future__ import annotations

from enum import StrEnum
from typing import TypeVar

from src.domain.errors.enum_parsing_error import EnumParsingError
from src.domain.formatters.enum_error_formatter import EnumErrorFormatter

EnumT = TypeVar(
    "EnumT",
    bound=StrEnum,
)


class EnumParsingErrorFactory:
    """
    Enum parsing exception factory.
    """

    @staticmethod
    def invalid_enum(
        *,
        field_name: str,
        value: object,
        enum_class: type[EnumT],
    ) -> EnumParsingError:
        message = EnumErrorFormatter.format_invalid_enum_error(
            field_name=field_name,
            value=value,
            enum_class=enum_class,
        )

        return EnumParsingError(message)