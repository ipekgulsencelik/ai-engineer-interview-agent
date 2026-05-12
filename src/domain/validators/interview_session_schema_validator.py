from __future__ import annotations

import math
from datetime import datetime

from src.domain.validation.interview_session_validation_schema import (
    INTERVIEW_SESSION_VALIDATION_SCHEMA,
)


class InterviewSessionSchemaValidator:
    @classmethod
    def validate(cls, payload: dict[str, object]) -> None:
        cls._validate_required_fields(payload)

        for field_name, rules in INTERVIEW_SESSION_VALIDATION_SCHEMA.items():
            value = payload[field_name]
            cls._validate_field_type(
                field_name=field_name,
                value=value,
                expected_type=rules.get("type"),
            )

            if rules.get("non_empty"):
                cls._validate_non_empty(
                    field_name=field_name,
                    value=value,
                )

            if "item_type" in rules:
                cls._validate_item_types(
                    field_name=field_name,
                    value=value,
                    expected_item_type=rules["item_type"],
                )

            if rules.get("finite"):
                cls._validate_finite_values(
                    field_name=field_name,
                    value=value,
                )

            if "min_value" in rules or "max_value" in rules:
                cls._validate_numeric_range(
                    field_name=field_name,
                    value=value,
                    min_value=rules.get("min_value"),
                    max_value=rules.get("max_value"),
                )

            if rules.get("timezone_aware"):
                cls._validate_timezone_aware_datetime(
                    field_name=field_name,
                    value=value,
                )

    @staticmethod
    def _validate_required_fields(payload: dict[str, object]) -> None:
        missing_fields = [
            field_name
            for field_name in INTERVIEW_SESSION_VALIDATION_SCHEMA
            if field_name not in payload
        ]

        if missing_fields:
            raise KeyError(
                f"Missing required fields: {', '.join(missing_fields)}"
            )

    @staticmethod
    def _validate_field_type(
        *,
        field_name: str,
        value: object,
        expected_type: object,
    ) -> None:
        if expected_type is None:
            return

        if not isinstance(value, expected_type):  # type: ignore[arg-type]
            raise TypeError(
                f"{field_name} must be of type {expected_type}."
            )

    @staticmethod
    def _validate_non_empty(
        *,
        field_name: str,
        value: object,
    ) -> None:
        if isinstance(value, str) and not value.strip():
            raise ValueError(f"{field_name} cannot be empty.")

    @staticmethod
    def _validate_item_types(
        *,
        field_name: str,
        value: object,
        expected_item_type: object,
    ) -> None:
        if not isinstance(value, tuple):
            raise TypeError(f"{field_name} must be a tuple.")

        for item in value:
            if not isinstance(item, expected_item_type):  # type: ignore[arg-type]
                raise TypeError(
                    f"All {field_name} items must be {expected_item_type}."
                )

    @staticmethod
    def _validate_finite_values(
        *,
        field_name: str,
        value: object,
    ) -> None:
        if not isinstance(value, tuple):
            raise TypeError(f"{field_name} must be a tuple.")

        for item in value:
            if isinstance(item, (int, float)) and not math.isfinite(item):
                raise ValueError(
                    f"{field_name} cannot contain NaN or infinity."
                )

    @staticmethod
    def _validate_numeric_range(
        *,
        field_name: str,
        value: object,
        min_value: float | None,
        max_value: float | None,
    ) -> None:
        if not isinstance(value, tuple):
            raise TypeError(f"{field_name} must be a tuple.")

        for item in value:
            if not isinstance(item, (int, float)):
                raise TypeError(
                    f"All {field_name} items must be numeric."
                )

            if min_value is not None and item < min_value:
                raise ValueError(
                    f"{field_name} items must be >= {min_value}."
                )

            if max_value is not None and item > max_value:
                raise ValueError(
                    f"{field_name} items must be <= {max_value}."
                )

    @staticmethod
    def _validate_timezone_aware_datetime(
        *,
        field_name: str,
        value: object,
    ) -> None:
        if not isinstance(value, datetime):
            raise TypeError(f"{field_name} must be a datetime.")

        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError(
                f"{field_name} must be timezone-aware."
            )