from __future__ import annotations

from typing import Any

from src.infrastructure.errors.validation_error import (
    ValidationError,
)
from src.infrastructure.validations.schema_types import (
    SchemaRule,
)


class StringListRuleValidator:
    """
    Generic string list schema rule validator.
    """

    @classmethod
    def validate_and_normalize(
        cls,
        *,
        field_name: str,
        value: Any,
        rules: SchemaRule,
    ) -> list[str]:
        cls._validate_type(
            field_name=field_name,
            value=value,
            rules=rules,
        )

        cls._validate_not_empty(
            field_name=field_name,
            value=value,
            rules=rules,
        )

        return cls._validate_items_and_normalize(
            field_name=field_name,
            value=value,
            rules=rules,
        )

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
                f"{field_name} must be a list."
            )

    @staticmethod
    def _validate_not_empty(
        *,
        field_name: str,
        value: list[object],
        rules: SchemaRule,
    ) -> None:
        if (
            rules.get("allow_empty") is False
            and not value
        ):
            raise ValidationError(
                f"{field_name} cannot be empty."
            )

    @staticmethod
    def _validate_items_and_normalize(
        *,
        field_name: str,
        value: list[object],
        rules: SchemaRule,
    ) -> list[str]:
        item_type = rules.get("item_type")
        normalized_items: list[str] = []

        for item in value:
            if (
                item_type is not None
                and not isinstance(item, item_type)
            ):
                raise ValidationError(
                    f"{field_name} must contain only strings."
                )

            normalized_item = (
                item.strip()
                if rules.get("strip_items") is True
                else item
            )

            if (
                rules.get("strip_items") is True
                and not normalized_item
            ):
                raise ValidationError(
                    f"{field_name} cannot contain empty strings."
                )

            normalized_items.append(normalized_item)

        return normalized_items