from __future__ import annotations

import math
from dataclasses import fields
from typing import TYPE_CHECKING

from src.application.validation.llm_request_validation_schema import (
    LLM_REQUEST_VALIDATION_SCHEMA,
)
from src.domain.validation.schema_types import (
    ValidationRule,
)

if TYPE_CHECKING:
    from src.application.models.llm_request import (
        LLMRequest,
    )


class LLMRequestValidator:
    """
    LLMRequest invariant validation helper.
    """

    @classmethod
    def validate(
        cls,
        request: "LLMRequest",
    ) -> None:
        cls._validate_model_type(
            request,
        )

        for model_field in fields(request):
            field_name = model_field.name
            value = getattr(
                request,
                field_name,
            )

            rules = LLM_REQUEST_VALIDATION_SCHEMA[
                field_name
            ]

            cls._validate_nullable(
                field_name=field_name,
                value=value,
                rules=rules,
            )

            if value is None:
                continue

            cls._validate_type(
                field_name=field_name,
                value=value,
                rules=rules,
            )

            cls._validate_non_empty_string(
                field_name=field_name,
                value=value,
                rules=rules,
            )

            cls._validate_numeric_bounds(
                field_name=field_name,
                value=value,
                rules=rules,
            )

            cls._validate_tuple_items(
                field_name=field_name,
                value=value,
                rules=rules,
            )

    @staticmethod
    def _validate_model_type(
        request: object,
    ) -> None:
        from src.application.models.llm_request import (
            LLMRequest,
        )

        if not isinstance(
            request,
            LLMRequest,
        ):
            raise TypeError(
                "request must be an LLMRequest instance."
            )

    @staticmethod
    def _validate_nullable(
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
    def _validate_type(
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

        if not isinstance(
            value,
            expected_type,
        ):
            expected_type_name = getattr(
                expected_type,
                "__name__",
                str(expected_type),
            )

            raise TypeError(
                f"{field_name} must be {expected_type_name}."
            )

    @staticmethod
    def _validate_non_empty_string(
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
    def _validate_numeric_bounds(
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
    def _validate_tuple_items(
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