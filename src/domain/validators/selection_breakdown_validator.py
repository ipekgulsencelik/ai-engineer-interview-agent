from __future__ import annotations

import math
from dataclasses import fields
from typing import TYPE_CHECKING, Any

from src.domain.validation.selection_breakdown_validation_schema import (
    SELECTION_BREAKDOWN_VALIDATION_SCHEMA,
)

if TYPE_CHECKING:
    from src.domain.results.selection_breakdown import SelectionBreakdown


class SelectionBreakdownValidator:
    """
    SelectionBreakdown domain modelinin invariant kurallarını doğrular.

    Bu validator:
        - SelectionBreakdown model type kontrolü yapar
        - score field type validation yapar
        - NaN / infinity değerlerini reddeder
        - numeric alanlarda bool değerlerini reddeder
        - normalized score boundary validation yapar
        - final_score minimum boundary validation yapar

    Validation kuralları:
        SELECTION_BREAKDOWN_VALIDATION_SCHEMA üzerinden okunur.
    """

    @classmethod
    def validate(
        cls,
        breakdown: "SelectionBreakdown",
    ) -> None:
        """
        SelectionBreakdown modelini schema tabanlı domain kurallarına göre
        validate eder.
        """

        cls._validate_model_type(breakdown)

        for model_field in fields(breakdown):
            field_name = model_field.name
            value = getattr(breakdown, field_name)

            rules = SELECTION_BREAKDOWN_VALIDATION_SCHEMA.get(
                field_name,
                {},
            )

            cls._validate_nullable(
                field_name=field_name,
                value=value,
                nullable=rules.get("nullable", False),
            )

            if value is None and rules.get("nullable", False):
                continue

            cls._validate_expected_type(
                field_name=field_name,
                value=value,
                expected_type=rules.get("type"),
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

            if "max_value" in rules:
                cls._validate_max_value(
                    field_name=field_name,
                    value=value,
                    max_value=rules["max_value"],
                )

    @staticmethod
    def _validate_model_type(
        breakdown: "SelectionBreakdown",
    ) -> None:
        from src.domain.results.selection_breakdown import SelectionBreakdown

        if not isinstance(breakdown, SelectionBreakdown):
            raise TypeError(
                "breakdown must be a SelectionBreakdown instance."
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
        value: float,
        min_value: float,
    ) -> None:
        if value < min_value:
            raise ValueError(
                f"{field_name} must be greater than or equal to "
                f"{min_value}."
            )

    @staticmethod
    def _validate_max_value(
        *,
        field_name: str,
        value: float,
        max_value: float,
    ) -> None:
        if value > max_value:
            raise ValueError(
                f"{field_name} must be less than or equal to "
                f"{max_value}."
            )