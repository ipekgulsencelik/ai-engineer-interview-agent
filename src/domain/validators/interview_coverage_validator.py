from __future__ import annotations

from dataclasses import fields

from src.domain.validation.interview_coverage_validation_schema import (
    INTERVIEW_COVERAGE_VALIDATION_SCHEMA,
)
from src.domain.validation.schema_types import (
    ValidationRule,
)


class InterviewCoverageValidator:
    """
    InterviewCoverage invariant validator.
    """

    @classmethod
    def validate(
        cls,
        coverage: object,
    ) -> None:
        from src.domain.value_objects.interview_coverage import (
            InterviewCoverage,
        )

        if not isinstance(coverage, InterviewCoverage):
            raise TypeError(
                "coverage must be InterviewCoverage."
            )

        for model_field in fields(coverage):
            field_name = model_field.name
            value = getattr(coverage, field_name)
            rules = INTERVIEW_COVERAGE_VALIDATION_SCHEMA[
                field_name
            ]

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

            cls._validate_count_mapping(
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
        expected_type = rules.get("type")

        if (
            expected_type is not None
            and not isinstance(value, expected_type)
        ):
            raise TypeError(
                f"{field_name} has invalid type."
            )

    @classmethod
    def _validate_count_mapping(
        cls,
        *,
        field_name: str,
        value: object,
        rules: ValidationRule,
    ) -> None:
        if not isinstance(value, dict):
            return

        key_type = rules.get("key_type")
        value_type = rules.get("value_type")

        for key, count in value.items():
            if (
                key_type is not None
                and not isinstance(key, key_type)
            ):
                raise TypeError(
                    f"{field_name} keys have invalid type."
                )

            if (
                rules.get("reject_bool_values") is True
                and isinstance(count, bool)
            ):
                raise TypeError(
                    f"{field_name} values cannot be bool."
                )

            if (
                value_type is not None
                and not isinstance(count, value_type)
            ):
                raise TypeError(
                    f"{field_name} values have invalid type."
                )

            cls._validate_min_value(
                field_name=field_name,
                value=count,
                rules=rules,
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

        if isinstance(value, dict):
            return

        if float(value) < float(min_value):
            raise ValueError(
                f"{field_name} must be greater than or equal to "
                f"{min_value}."
            )