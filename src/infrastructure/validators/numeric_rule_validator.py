from __future__ import annotations

import math
from typing import Any

from src.infrastructure.errors.validation_error import (
    ValidationError,
)
from src.infrastructure.validations.schema_types import (
    SchemaRule,
)


class NumericRuleValidator:
    """
    Generic numeric schema rule validator.

    Tek responsibility:
        - numeric schema rule validation orchestration

    Alt kontroller private method'lara ayrılmıştır.
    """

    @classmethod
    def validate(
        cls,
        *,
        field_name: str,
        value: Any,
        rules: SchemaRule,
    ) -> None:
        cls._validate_type(
            field_name=field_name,
            value=value,
            rules=rules,
        )

        numeric_value = cls._to_finite_float(
            field_name=field_name,
            value=value,
        )

        cls._validate_range(
            field_name=field_name,
            numeric_value=numeric_value,
            rules=rules,
        )

    @staticmethod
    def _validate_type(
        *,
        field_name: str,
        value: Any,
        rules: SchemaRule,
    ) -> None:
        expected_type = rules.get("type")

        if (
            rules.get("allow_bool") is False
            and isinstance(value, bool)
        ):
            raise ValidationError(
                f"{field_name} must not be a boolean."
            )

        if (
            expected_type is not None
            and not isinstance(value, expected_type)
        ):
            raise ValidationError(
                f"{field_name} has invalid type."
            )

    @staticmethod
    def _to_finite_float(
        *,
        field_name: str,
        value: Any,
    ) -> float:
        numeric_value = float(value)

        if not math.isfinite(numeric_value):
            raise ValidationError(
                f"{field_name} must be finite."
            )

        return numeric_value

    @staticmethod
    def _validate_range(
        *,
        field_name: str,
        numeric_value: float,
        rules: SchemaRule,
    ) -> None:
        min_value = rules.get("min_value")
        max_value = rules.get("max_value")

        if (
            min_value is not None
            and numeric_value < float(min_value)
        ):
            raise ValidationError(
                f"{field_name} must be greater than or equal to "
                f"{min_value}."
            )

        if (
            max_value is not None
            and numeric_value > float(max_value)
        ):
            raise ValidationError(
                f"{field_name} must be less than or equal to "
                f"{max_value}."
            )