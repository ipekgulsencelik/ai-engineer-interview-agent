from __future__ import annotations

from dataclasses import fields
from typing import TYPE_CHECKING, Any

from src.application.validation.llm_response_validation_schema import (
    LLM_RESPONSE_VALIDATION_SCHEMA,
)

if TYPE_CHECKING:
    from src.application.models.llm_response import (
        LLMResponse,
    )


class LLMResponseValidator:
    """
    LLMResponse domain invariant validation işlemlerini yapar.
    """

    @classmethod
    def validate(
        cls,
        response: "LLMResponse",
    ) -> None:
        cls._validate_model_type(response)

        for model_field in fields(response):
            field_name = model_field.name
            value = getattr(response, field_name)

            rules = LLM_RESPONSE_VALIDATION_SCHEMA.get(
                field_name,
                {},
            )

            nullable = rules.get("nullable", False)

            cls._validate_nullable(
                field_name=field_name,
                value=value,
                nullable=nullable,
            )

            if value is None and nullable:
                continue

            cls._validate_expected_type(
                field_name=field_name,
                value=value,
                expected_type=rules.get("type"),
            )

            if rules.get("non_empty", False):
                cls._validate_non_empty_string(
                    field_name=field_name,
                    value=value,
                )

    @staticmethod
    def _validate_model_type(
        response: "LLMResponse",
    ) -> None:
        from src.application.models.llm_response import (
            LLMResponse,
        )

        if not isinstance(response, LLMResponse):
            raise TypeError(
                "response must be an LLMResponse instance."
            )

    @staticmethod
    def _validate_nullable(
        *,
        field_name: str,
        value: object,
        nullable: bool,
    ) -> None:
        if value is None and not nullable:
            raise TypeError(
                f"{field_name} cannot be None."
            )

    @staticmethod
    def _validate_expected_type(
        *,
        field_name: str,
        value: object,
        expected_type: Any,
    ) -> None:
        if expected_type is None:
            return

        if expected_type is not bool and isinstance(value, bool):
            raise TypeError(
                f"{field_name} cannot be bool."
            )

        if not isinstance(value, expected_type):
            raise TypeError(
                f"{field_name} must be {expected_type}."
            )

    @staticmethod
    def _validate_non_empty_string(
        *,
        field_name: str,
        value: str,
    ) -> None:
        if not value.strip():
            raise ValueError(
                f"{field_name} cannot be empty."
            )