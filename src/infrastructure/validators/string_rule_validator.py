from __future__ import annotations

from typing import Any

from src.infrastructure.errors.validation_error import (
    ValidationError,
)
from src.infrastructure.validations.schema_types import (
    SchemaRule,
)


class StringRuleValidator:
    """
    Generic string schema rule validator.
    """

    @classmethod
    def validate_and_normalize(
        cls,
        *,
        field_name: str,
        value: Any,
        rules: SchemaRule,
    ) -> str:
        cls._validate_type(
            field_name=field_name,
            value=value,
            rules=rules,
        )

        normalized_value = cls._normalize(
            value=value,
            rules=rules,
        )

        cls._validate_non_empty(
            field_name=field_name,
            value=normalized_value,
            rules=rules,
        )

        return normalized_value

    @staticmethod
    def _validate_type(
        *,
        field_name: str,
        value: Any,
        rules: SchemaRule,
    ) -> None:
        expected_type = rules.get("type")

        if (
            expected_type is not None
            and not isinstance(value, expected_type)
        ):
            raise ValidationError(
                f"{field_name} must be a string."
            )

    @staticmethod
    def _normalize(
        *,
        value: str,
        rules: SchemaRule,
    ) -> str:
        if rules.get("strip") is True:
            return value.strip()

        return value

    @staticmethod
    def _validate_non_empty(
        *,
        field_name: str,
        value: str,
        rules: SchemaRule,
    ) -> None:
        if (
            rules.get("non_empty", False)
            and not value
        ):
            raise ValidationError(
                f"{field_name} cannot be empty."
            )