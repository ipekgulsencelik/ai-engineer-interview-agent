from __future__ import annotations

import math
from dataclasses import fields
from typing import TYPE_CHECKING, Any

from src.application.validation.llm_response_metadata_validation_schema import (
    LLM_RESPONSE_METADATA_VALIDATION_SCHEMA,
)

if TYPE_CHECKING:
    from src.application.models.llm_response_metadata import (
        LLMResponseMetadata,
    )


class LLMResponseMetadataValidator:
    """
    LLMResponseMetadata validation işlemlerini yapar.
    """

    @classmethod
    def validate(
        cls,
        metadata: "LLMResponseMetadata",
    ) -> None:
        cls._validate_model_type(metadata)

        for model_field in fields(metadata):
            field_name = model_field.name
            value = getattr(metadata, field_name)

            rules = (
                LLM_RESPONSE_METADATA_VALIDATION_SCHEMA.get(
                    field_name,
                    {},
                )
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

            if rules.get("finite", False):
                cls._validate_finite(
                    field_name=field_name,
                    value=value,
                )

            if "min_value" in rules:
                cls._validate_min_value(
                    field_name=field_name,
                    value=value,
                    min_value=rules["min_value"],
                )

    @staticmethod
    def _validate_model_type(
        metadata: "LLMResponseMetadata",
    ) -> None:
        from src.application.models.llm_response_metadata import (
            LLMResponseMetadata,
        )

        if not isinstance(metadata, LLMResponseMetadata):
            raise TypeError(
                "metadata must be an "
                "LLMResponseMetadata instance."
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

    @staticmethod
    def _validate_finite(
        *,
        field_name: str,
        value: float,
    ) -> None:
        if not math.isfinite(value):
            raise ValueError(
                f"{field_name} must be finite."
            )

    @staticmethod
    def _validate_min_value(
        *,
        field_name: str,
        value: int | float,
        min_value: int | float,
    ) -> None:
        if value < min_value:
            raise ValueError(
                f"{field_name} must be greater than "
                f"or equal to {min_value}."
            )