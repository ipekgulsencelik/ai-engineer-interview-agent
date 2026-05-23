from __future__ import annotations

import math
from dataclasses import fields
from typing import TYPE_CHECKING

from src.application.validation.llm_response_metadata_validation_schema import (
    LLM_RESPONSE_METADATA_VALIDATION_SCHEMA,
)
from src.domain.validation.schema_types import (
    ValidationRule,
)

if TYPE_CHECKING:
    from src.application.models.llm_response_metadata import (
        LLMResponseMetadata,
    )


class LLMResponseMetadataValidator:
    """
    LLMResponseMetadata validation helper.
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

            rules = LLM_RESPONSE_METADATA_VALIDATION_SCHEMA[
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

            cls._validate_finite(
                field_name=field_name,
                value=value,
                rules=rules,
            )

            cls._validate_min_value(
                field_name=field_name,
                value=value,
                rules=rules,
            )

    @staticmethod
    def _validate_model_type(
        metadata: object,
    ) -> None:
        from src.application.models.llm_response_metadata import (
            LLMResponseMetadata,
        )

        if not isinstance(metadata, LLMResponseMetadata):
            raise TypeError(
                "metadata must be an LLMResponseMetadata instance."
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

        if not isinstance(value, expected_type):
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

    @staticmethod
    def _validate_finite(
        *,
        field_name: str,
        value: object,
        rules: ValidationRule,
    ) -> None:
        if rules.get("finite") is not True:
            return

        try:
            numeric_value = float(value)

        except (TypeError, ValueError) as exc:
            raise TypeError(
                f"{field_name} must be numeric."
            ) from exc

        if not math.isfinite(numeric_value):
            raise ValueError(
                f"{field_name} must be finite."
            )

    @staticmethod
    def _validate_min_value(
        *,
        field_name: str,
        value: object,
        rules: ValidationRule,
    ) -> None:
        min_value = rules.get("min_value")

        if min_value is None:
            return

        try:
            numeric_value = float(value)

        except (TypeError, ValueError) as exc:
            raise TypeError(
                f"{field_name} must be numeric."
            ) from exc

        if numeric_value < float(min_value):
            raise ValueError(
                f"{field_name} must be greater than or equal to "
                f"{min_value}."
            )