from __future__ import annotations

import math
from dataclasses import fields
from typing import Any

from src.domain.models.selection_breakdown import (
    SelectionBreakdown,
)
from src.domain.validation.selection_breakdown_validation_schema import (
    SELECTION_BREAKDOWN_VALIDATION_SCHEMA,
)


class SelectionBreakdownValidator:
    """
    SelectionBreakdown invariant validator.
    """

    @classmethod
    def validate(
        cls,
        breakdown: SelectionBreakdown,
    ) -> None:
        cls._validate_model_type(
            breakdown=breakdown,
        )

        for model_field in fields(breakdown):
            field_name = model_field.name

            value = getattr(
                breakdown,
                field_name,
            )

            rules = (
                SELECTION_BREAKDOWN_VALIDATION_SCHEMA[
                    field_name
                ]
            )

            cls._validate_type(
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

            cls._validate_max_value(
                field_name=field_name,
                value=value,
                rules=rules,
            )

    @staticmethod
    def _validate_model_type(
        *,
        breakdown: object,
    ) -> None:
        if not isinstance(
            breakdown,
            SelectionBreakdown,
        ):
            raise TypeError(
                "breakdown must be SelectionBreakdown."
            )

    @staticmethod
    def _validate_type(
        *,
        field_name: str,
        value: object,
        rules: dict[str, Any],
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
            and not isinstance(value, expected_type)
        ):
            raise TypeError(
                f"{field_name} has invalid type."
            )

    @staticmethod
    def _validate_finite(
        *,
        field_name: str,
        value: object,
        rules: dict[str, Any],
    ) -> None:
        if rules.get("finite") is not True:
            return

        if not math.isfinite(float(value)):
            raise ValueError(
                f"{field_name} must be finite."
            )

    @staticmethod
    def _validate_min_value(
        *,
        field_name: str,
        value: object,
        rules: dict[str, Any],
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
        rules: dict[str, Any],
    ) -> None:
        max_value = rules.get("max_value")

        if max_value is None:
            return

        if float(value) > float(max_value):
            raise ValueError(
                f"{field_name} must be less than or equal to "
                f"{max_value}."
            )