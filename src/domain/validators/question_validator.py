from __future__ import annotations

import math
from dataclasses import fields
from typing import TYPE_CHECKING, Any

from src.domain.errors.question_validation_error import (
    QuestionValidationError,
)
from src.domain.validation.question_validation_schema import (
    QUESTION_VALIDATION_SCHEMA,
)

if TYPE_CHECKING:
    from src.domain.entities.question import Question


class QuestionValidator:
    """
    Question entity'sinin domain invariant kurallarını validate eder.
    """

    @classmethod
    def validate(
        cls,
        question: "Question",
    ) -> None:
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
            raise QuestionValidationError(
                "question must be a Question instance."
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
            raise QuestionValidationError(
                f"{field_name} cannot be bool."
            )

        if not isinstance(value, expected_type):
            raise QuestionValidationError(
                f"{field_name} must be {expected_type}."
            )

    @staticmethod
    def _validate_finite(
        *,
        field_name: str,
        value: object,
    ) -> None:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise QuestionValidationError(
                f"{field_name} must be a finite number."
            )

        if not math.isfinite(float(value)):
            raise QuestionValidationError(
                f"{field_name} must be finite."
            )

    @staticmethod
    def _validate_non_empty(
        *,
        field_name: str,
        value: object,
    ) -> None:
        if not isinstance(value, str):
            raise QuestionValidationError(
                f"{field_name} must be a string."
            )

        if not value.strip():
            raise QuestionValidationError(
                f"{field_name} cannot be empty."
            )

    @staticmethod
    def _validate_list_items(
        *,
        field_name: str,
        value: object,
        item_type: type,
    ) -> None:
        if not isinstance(value, list):
            raise QuestionValidationError(
                f"{field_name} must be a list."
            )

        for item in value:
            if not isinstance(item, item_type):
                raise QuestionValidationError(
                    f"All items in {field_name} must be {item_type}."
                )

            if item_type is str and not item.strip():
                raise QuestionValidationError(
                    f"Items in {field_name} cannot be empty."
                )

    @staticmethod
    def _validate_min_value(
        *,
        field_name: str,
        value: object,
        min_value: float,
    ) -> None:
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise QuestionValidationError(
                f"{field_name} must be numeric."
            )

        if float(value) < min_value:
            raise QuestionValidationError(
                f"{field_name} must be greater than or equal to "
                f"{min_value}."
            )

    @staticmethod
    def _validate_max_value(
        *,
        field_name: str,
        value: object,
        max_value: float,
    ) -> None:
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise QuestionValidationError(
                f"{field_name} must be numeric."
            )

        if float(value) > max_value:
            raise QuestionValidationError(
                f"{field_name} must be less than or equal to "
                f"{max_value}."
            )