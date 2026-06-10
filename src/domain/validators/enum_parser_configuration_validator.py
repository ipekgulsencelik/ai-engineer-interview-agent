from __future__ import annotations


class EnumParserConfigurationValidator:
    """
    Enum parser configuration validation rules.
    """

    @staticmethod
    def validate_field_name(
        *,
        field_name: str,
    ) -> None:
        if not isinstance(field_name, str):
            raise TypeError(
                "field_name must be a string."
            )

        if not field_name.strip():
            raise ValueError(
                "field_name cannot be empty."
            )