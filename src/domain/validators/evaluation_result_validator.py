from __future__ import annotations

import math
from dataclasses import fields
from typing import TYPE_CHECKING, Any

from src.domain.validation.evaluation_result_validation_schema import (
    EVALUATION_RESULT_VALIDATION_SCHEMA,
)

if TYPE_CHECKING:
    from src.domain.results.evaluation_result import EvaluationResult


class EvaluationResultValidator:
    """
    EvaluationResult domain invariant validation işlemlerini yapar.
    """

    @classmethod
    def validate(
        cls,
        result: "EvaluationResult",
    ) -> None:
        cls._validate_model_type(result)

        for model_field in fields(result):
            field_name = model_field.name
            value = getattr(result, field_name)

            rules = EVALUATION_RESULT_VALIDATION_SCHEMA.get(
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

            if rules.get("non_empty", False):
                cls._validate_non_empty_string(
                    field_name=field_name,
                    value=value,
                    strip=rules.get("strip", False),
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
        result: "EvaluationResult",
    ) -> None:
        from src.domain.results.evaluation_result import (
            EvaluationResult,
        )

        if not isinstance(result, EvaluationResult):
            raise TypeError(
                "result must be an EvaluationResult instance."
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
    def _validate_non_empty_string(
        *,
        field_name: str,
        value: str,
        strip: bool,
    ) -> None:
        normalized_value = value.strip() if strip else value

        if not normalized_value:
            raise ValueError(
                f"{field_name} cannot be empty."
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
                f"{field_name} must be greater than or equal "
                f"to {min_value}."
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
                f"{field_name} must be less than or equal "
                f"to {max_value}."
            )