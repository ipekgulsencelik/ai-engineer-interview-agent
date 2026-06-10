from __future__ import annotations

import math

from src.domain.validation.schema_types import (
    ValidationRule,
)


class BaseSchemaValidator:
    """
    Reusable schema-driven validation helper.
    """

    @staticmethod
    def validate_model_type(
        *,
        value: object,
        expected_type: type,
        field_name: str = "value",
    ) -> None:
        if not isinstance(value, expected_type):
            raise TypeError(
                f"{field_name} must be an "
                f"{expected_type.__name__} instance."
            )

    @staticmethod
    def validate_nullable(
        *,
        field_name: str,
        value: object,
        rules: ValidationRule,
    ) -> None:
        if (
            value is None
            and rules.get("nullable") is not True
        ):
            raise TypeError(
                f"{field_name} cannot be None."
            )

    @staticmethod
    def validate_type(
        *,
        field_name: str,
        value: object,
        rules: ValidationRule,
    ) -> None:
        if (
            rules.get("reject_bool") is True
            and isinstance(value, bool)
        ):
            raise TypeError(
                f"{field_name} cannot be bool."
            )

        expected_type = rules.get("type")

        if expected_type is None:
            return

        if not isinstance(value, expected_type):
            raise TypeError(
                f"{field_name} has invalid type."
            )

    @staticmethod
    def validate_non_empty_string(
        *,
        field_name: str,
        value: object,
        rules: ValidationRule,
    ) -> None:
        if rules.get("non_empty") is not True:
            return

        if not isinstance(value, str):
            raise TypeError(
                f"{field_name} must be a string."
            )

        if not value.strip():
            raise ValueError(
                f"{field_name} cannot be empty."
            )

    @staticmethod
    def validate_numeric_bounds(
        *,
        field_name: str,
        value: object,
        rules: ValidationRule,
    ) -> None:
        if (
            rules.get("finite") is not True
            and "min_value" not in rules
            and "max_value" not in rules
        ):
            return

        try:
            numeric_value = float(value)

        except (TypeError, ValueError) as exc:
            raise TypeError(
                f"{field_name} must be numeric."
            ) from exc

        if (
            rules.get("finite") is True
            and not math.isfinite(numeric_value)
        ):
            raise ValueError(
                f"{field_name} must be finite."
            )

        min_value = rules.get("min_value")
        max_value = rules.get("max_value")

        if (
            min_value is not None
            and numeric_value < float(min_value)
        ):
            raise ValueError(
                f"{field_name} must be greater than or equal to "
                f"{min_value}."
            )

        if (
            max_value is not None
            and numeric_value > float(max_value)
        ):
            raise ValueError(
                f"{field_name} must be less than or equal to "
                f"{max_value}."
            )

    @staticmethod
    def validate_tuple_items(
        *,
        field_name: str,
        value: object,
        rules: ValidationRule,
    ) -> None:
        if not isinstance(value, tuple):
            return

        item_type = rules.get("item_type")

        for item in value:
            if (
                rules.get("reject_bool_items") is True
                and isinstance(item, bool)
            ):
                raise TypeError(
                    f"{field_name} items cannot be bool."
                )

            if (
                item_type is not None
                and not isinstance(item, item_type)
            ):
                raise TypeError(
                    f"{field_name} items have invalid type."
                )

            if (
                rules.get("non_empty_items") is True
                and isinstance(item, str)
                and not item.strip()
            ):
                raise ValueError(
                    f"{field_name} items cannot be empty."
                )


    @staticmethod
    def validate_has_callable(
        *,
        value: object,
        method_name: str,
        field_name: str,
    ) -> None:
        method = getattr(
            value,
            method_name,
            None,
        )

        if not callable(method):
            raise TypeError(
                f"{field_name} must implement callable "
                f"{method_name}()."
            )