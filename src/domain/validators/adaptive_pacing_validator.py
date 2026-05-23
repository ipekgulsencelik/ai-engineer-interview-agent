from __future__ import annotations

from dataclasses import fields

from src.domain.validation.adaptive_pacing_validation_schema import (
    ADAPTIVE_PACING_VALIDATION_SCHEMA,
)
from src.domain.validation.schema_types import (
    ValidationRule,
)


class AdaptivePacingValidator:
    """
    AdaptivePacing invariant validator.
    """

    @classmethod
    def validate(
        cls,
        pacing: object,
    ) -> None:
        from src.domain.value_objects.adaptive_pacing import (
            AdaptivePacing,
        )

        if not isinstance(pacing, AdaptivePacing):
            raise TypeError(
                "pacing must be AdaptivePacing."
            )

        for model_field in fields(pacing):
            field_name = model_field.name

            value = getattr(
                pacing,
                field_name,
            )

            rules = (
                ADAPTIVE_PACING_VALIDATION_SCHEMA[
                    field_name
                ]
            )

            cls._validate_nullable(
                field_name=field_name,
                value=value,
                rules=rules,
            )

            cls._validate_type(
                field_name=field_name,
                value=value,
                rules=rules,
            )

            cls._validate_min_value(
                field_name=field_name,
                value=value,
                rules=rules,
            )

            cls._validate_max_value(
                field_name=field_name,
                value=value,
                rules=rules,
            )

            cls._validate_strictly_positive(
                field_name=field_name,
                value=value,
                rules=rules,
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

        if (
            expected_type is not None
            and not isinstance(
                value,
                expected_type,
            )
        ):
            raise TypeError(
                f"{field_name} has invalid type."
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

        if float(value) < float(min_value):
            raise ValueError(
                f"{field_name} must be greater than or equal to "
                f"{min_value}."
            )

    @staticmethod
    def _validate_max_value(
        *,
        field_name: str,
        value: object,
        rules: ValidationRule,
    ) -> None:
        max_value = rules.get("max_value")

        if max_value is None:
            return

        if float(value) > float(max_value):
            raise ValueError(
                f"{field_name} must be less than or equal to "
                f"{max_value}."
            )

    @staticmethod
    def _validate_strictly_positive(
        *,
        field_name: str,
        value: object,
        rules: ValidationRule,
    ) -> None:
        if (
            rules.get("strictly_positive")
            is not True
        ):
            return

        if float(value) <= 0:
            raise ValueError(
                f"{field_name} must be greater than zero."
            )