from __future__ import annotations

import math
from dataclasses import fields
from typing import TYPE_CHECKING, Any

from src.domain.validation.scoring_context_validation_schema import (
    SCORING_CONTEXT_VALIDATION_SCHEMA,
)

if TYPE_CHECKING:
    from src.domain.scoring.scoring_context import ScoringContext


class ScoringContextValidator:
    """
    ScoringContext domain invariant validation işlemlerini yapar.
    """

    @classmethod
    def validate(
        cls,
        context: "ScoringContext",
    ) -> None:
        cls._validate_model_type(context)

        for model_field in fields(context):
            field_name = model_field.name
            value = getattr(context, field_name)

            rules = SCORING_CONTEXT_VALIDATION_SCHEMA.get(
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

            if "item_type" in rules:
                cls._validate_list_items(
                    field_name=field_name,
                    value=value,
                    item_type=rules["item_type"],
                )

            if rules.get("finite_items", False):
                cls._validate_finite_items(
                    field_name=field_name,
                    value=value,
                )

            if "min_item_value" in rules:
                cls._validate_min_item_value(
                    field_name=field_name,
                    value=value,
                    min_value=rules["min_item_value"],
                )

            if "max_item_value" in rules:
                cls._validate_max_item_value(
                    field_name=field_name,
                    value=value,
                    max_value=rules["max_item_value"],
                )

    @staticmethod
    def _validate_model_type(
        context: "ScoringContext",
    ) -> None:
        from src.domain.scoring.scoring_context import ScoringContext

        if not isinstance(context, ScoringContext):
            raise TypeError(
                "context must be a ScoringContext instance."
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
    def _validate_list_items(
        *,
        field_name: str,
        value: list,
        item_type: type | tuple[type, ...],
    ) -> None:
        for item in value:
            if item_type in (int, float, (int, float)) and isinstance(item, bool):
                raise TypeError(
                    f"Items in {field_name} cannot be bool."
                )
        
            if not isinstance(item, item_type):
                raise TypeError(
                    f"All items in {field_name} must be {item_type}."
                )

            if item_type is str and not item.strip():
                raise ValueError(
                    f"Items in {field_name} cannot be empty."
                )

            if item_type in (int, float) and isinstance(item, bool):
                raise TypeError(
                    f"Items in {field_name} cannot be bool."
                )

    @staticmethod
    def _validate_finite_items(
        *,
        field_name: str,
        value: list,
    ) -> None:
        for item in value:
            if not math.isfinite(item):
                raise ValueError(
                    f"Items in {field_name} must be finite."
                )

    @staticmethod
    def _validate_min_item_value(
        *,
        field_name: str,
        value: list,
        min_value: float,
    ) -> None:
        for item in value:
            if item < min_value:
                raise ValueError(
                    f"Items in {field_name} must be greater than or "
                    f"equal to {min_value}."
                )

    @staticmethod
    def _validate_max_item_value(
        *,
        field_name: str,
        value: list,
        max_value: float,
    ) -> None:
        for item in value:
            if item > max_value:
                raise ValueError(
                    f"Items in {field_name} must be less than or equal "
                    f"to {max_value}."
                )