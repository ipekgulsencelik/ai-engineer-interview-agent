from __future__ import annotations

import math
from dataclasses import fields
from typing import TYPE_CHECKING, Any

from src.domain.validation.question_validation_schema import (
    QUESTION_VALIDATION_SCHEMA,
)

if TYPE_CHECKING:
    from src.domain.entities.question import Question


class QuestionValidator:
    """
    Question entity'sinin domain invariant kurallarını validate eder.

    Bu validator:
        - type validation
        - non-empty string validation
        - list item validation
        - numeric min/max validation
        - finite number validation
        - bool-as-number rejection

    işlemlerinden sorumludur.
    """

    @classmethod
    def validate(
        cls,
        question: "Question",
    ) -> None:
        """
        Question entity'sini validation schema'ya göre doğrular.
        """

        cls._validate_model_type(question)

        for model_field in fields(question):
            field_name = model_field.name
            value = getattr(question, field_name)

            metadata = QUESTION_VALIDATION_SCHEMA.get(
                field_name,
                {},
            )

            nullable = metadata.get(
                "nullable",
                False,
            )

            if value is None and nullable:
                continue

            cls._validate_expected_type(
                field_name=field_name,
                value=value,
                expected_type=metadata.get("type"),
            )

            if metadata.get("finite", False):
                cls._validate_finite(
                    field_name=field_name,
                    value=value,
                )

            if metadata.get("non_empty", False):
                cls._validate_non_empty(
                    field_name=field_name,
                    value=value,
                )

            if "item_type" in metadata:
                cls._validate_list_items(
                    field_name=field_name,
                    value=value,
                    item_type=metadata["item_type"],
                )

            if "min_value" in metadata:
                cls._validate_min_value(
                    field_name=field_name,
                    value=value,
                    min_value=metadata["min_value"],
                )

            if "max_value" in metadata:
                cls._validate_max_value(
                    field_name=field_name,
                    value=value,
                    max_value=metadata["max_value"],
                )

    @staticmethod
    def _validate_model_type(
        question: "Question",
    ) -> None:
        from src.domain.entities.question import Question

        if not isinstance(question, Question):
            raise TypeError("question must be a Question instance.")

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
            raise TypeError(f"{field_name} cannot be bool.")

        if not isinstance(value, expected_type):
            raise TypeError(f"{field_name} must be {expected_type}.")

    @staticmethod
    def _validate_finite(
        *,
        field_name: str,
        value: float,
    ) -> None:
        if not math.isfinite(value):
            raise ValueError(f"{field_name} must be finite.")

    @staticmethod
    def _validate_non_empty(
        *,
        field_name: str,
        value: str,
    ) -> None:
        if not value.strip():
            raise ValueError(f"{field_name} cannot be empty.")

    @staticmethod
    def _validate_list_items(
        *,
        field_name: str,
        value: list,
        item_type: type,
    ) -> None:
        for item in value:
            if not isinstance(item, item_type):
                raise TypeError(
                    f"All items in {field_name} must be {item_type}."
                )

            if item_type is str and not item.strip():
                raise ValueError(
                    f"Items in {field_name} cannot be empty."
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