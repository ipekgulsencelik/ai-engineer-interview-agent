from __future__ import annotations

from dataclasses import fields
from typing import TYPE_CHECKING

from src.application.validation.llm_response_validation_schema import (
    LLM_RESPONSE_VALIDATION_SCHEMA,
)
from src.domain.validation.schema_types import (
    ValidationRule,
)

if TYPE_CHECKING:
    from src.application.models.llm_response import (
        LLMResponse,
    )


class LLMResponseValidator:
    """
    LLMResponse invariant validation helper.
    """

    @classmethod
    def validate(
        cls,
        response: "LLMResponse",
    ) -> None:
        cls._validate_model_type(
            response,
        )

        for model_field in fields(response):
            field_name = model_field.name
            value = getattr(
                response,
                field_name,
            )

            rules = LLM_RESPONSE_VALIDATION_SCHEMA[
                field_name
            ]

            cls._validate_nullable(
                field_name=field_name,
                value=value,
                rules=rules,
            )

            if value is None:
                continue

            cls._validate_expected_type(
                field_name=field_name,
                value=value,
                rules=rules,
            )

            cls._validate_non_empty_string(
                field_name=field_name,
                value=value,
                rules=rules,
            )

    @staticmethod
    def _validate_model_type(
        response: object,
    ) -> None:
        from src.application.models.llm_response import (
            LLMResponse,
        )

        if not isinstance(
            response,
            LLMResponse,
        ):
            raise TypeError(
                "response must be an LLMResponse instance."
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
    def _validate_expected_type(
        *,
        field_name: str,
        value: object,
        rules: ValidationRule,
    ) -> None:
        expected_type = rules.get("type")

        if expected_type is None:
            return

        if (
            rules.get("reject_bool") is True
            and isinstance(value, bool)
        ):
            raise TypeError(
                f"{field_name} cannot be bool."
            )

        if not isinstance(
            value,
            expected_type,
        ):
            raise TypeError(
                f"{field_name} has invalid type."
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