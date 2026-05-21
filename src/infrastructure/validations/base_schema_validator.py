from __future__ import annotations

from typing import Any

from src.infrastructure.errors.validation_error import (
    ValidationError,
)
from src.infrastructure.validation.numeric_rule_validator import (
    NumericRuleValidator,
)
from src.infrastructure.validation.schema_types import (
    SchemaRule,
)
from src.infrastructure.validation.string_list_rule_validator import (
    StringListRuleValidator,
)
from src.infrastructure.validation.string_rule_validator import (
    StringRuleValidator,
)


class BaseSchemaValidator:
    """
    Generic schema-driven validation facade.
    """

    @staticmethod
    def validate_type(
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
                f"{field_name} has invalid type."
            )

    @staticmethod
    def validate_optional_string(
        *,
        field_name: str,
        value: str | None,
        rules: SchemaRule,
    ) -> None:
        if value is None:
            return

        StringRuleValidator.validate_and_normalize(
            field_name=field_name,
            value=value,
            rules=rules,
        )

    @staticmethod
    def validate_string_and_return(
        *,
        field_name: str,
        value: str,
        rules: SchemaRule,
    ) -> str:
        return StringRuleValidator.validate_and_normalize(
            field_name=field_name,
            value=value,
            rules=rules,
        )

    @staticmethod
    def validate_string_list_and_return(
        *,
        field_name: str,
        value: Any,
        rules: SchemaRule,
    ) -> list[str]:
        return StringListRuleValidator.validate_and_normalize(
            field_name=field_name,
            value=value,
            rules=rules,
        )

    @staticmethod
    def validate_numeric(
        *,
        field_name: str,
        value: Any,
        rules: SchemaRule,
    ) -> None:
        NumericRuleValidator.validate(
            field_name=field_name,
            value=value,
            rules=rules,
        )