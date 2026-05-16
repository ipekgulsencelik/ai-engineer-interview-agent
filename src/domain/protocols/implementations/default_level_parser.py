from __future__ import annotations

from src.domain.enums.level import Level
from src.domain.validators.enum_parser_validator import (
    EnumParserValidator,
)


class DefaultLevelParser:
    """
    Default Level parser implementation.
    """

    def parse(
        self,
        value: Level | str,
    ) -> Level:
        EnumParserValidator.validate_raw_enum_input(
            value=value,
            enum_class=Level,
            field_name="level",
        )

        if isinstance(value, Level):
            return value

        normalized_value = (
            value.strip().upper()
        )

        try:
            return Level(normalized_value)

        except ValueError as exc:
            allowed_values = ", ".join(
                item.value
                for item in Level
            )

            raise ValueError(
                f"Invalid level: {value}. "
                f"Expected one of: "
                f"{allowed_values}."
            ) from exc