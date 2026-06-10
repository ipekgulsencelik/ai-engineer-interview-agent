from __future__ import annotations

from dataclasses import fields
from math import isfinite

from src.domain.validation.interview_state_validation_schema import (
    INTERVIEW_STATE_VALIDATION_SCHEMA,
)
from src.domain.validation.schema_types import (
    ValidationRule,
)


class InterviewStateValidator:
    """
    InterviewState invariant validator.
    """

    @classmethod
    def validate(
        cls,
        state: object,
    ) -> None:
        from src.domain.value_objects.interview_state import (
            InterviewState,
        )

        if not isinstance(state, InterviewState):
            raise TypeError(
                "state must be InterviewState."
            )

        for model_field in fields(state):
            field_name = model_field.name

            value = getattr(
                state,
                field_name,
            )

            rules = (
                INTERVIEW_STATE_VALIDATION_SCHEMA[
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

            cls._validate_tuple_items(
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
        def _validate_tuple_items(
            *,
            field_name: str,
            value: object,
            rules: ValidationRule,
        ) -> None:
            if not isinstance(value, tuple):
                return

            item_type = rules.get("item_type")
            min_value = rules.get("min_value")
            max_value = rules.get("max_value")

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

                if isinstance(item, (int, float)):
                    if not isfinite(float(item)):
                        raise ValueError(
                            f"{field_name} items must be finite."
                        )

                    if (
                        min_value is not None
                        and float(item) < float(min_value)
                    ):
                        raise ValueError(
                            f"{field_name} items must be greater than or "
                            f"equal to {min_value}."
                        )

                    if (
                        max_value is not None
                        and float(item) > float(max_value)
                    ):
                        raise ValueError(
                            f"{field_name} items must be less than or "
                            f"equal to {max_value}."
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