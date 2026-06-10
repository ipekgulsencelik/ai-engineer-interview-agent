from __future__ import annotations

from dataclasses import fields

from src.domain.validation.question_fatigue_validation_schema import (
    QUESTION_FATIGUE_VALIDATION_SCHEMA,
)
from src.domain.validation.schema_types import (
    ValidationRule,
)


class QuestionFatigueValidator:
    """
    QuestionFatigue invariant validator.
    """

    @classmethod
    def validate(
        cls,
        fatigue: object,
    ) -> None:
        from src.domain.value_objects.question_fatigue import (
            QuestionFatigue,
        )

        if not isinstance(fatigue, QuestionFatigue):
            raise TypeError(
                "fatigue must be QuestionFatigue."
            )

        for model_field in fields(fatigue):
            field_name = model_field.name

            value = getattr(
                fatigue,
                field_name,
            )

            rules = (
                QUESTION_FATIGUE_VALIDATION_SCHEMA[
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