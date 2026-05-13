from __future__ import annotations

from dataclasses import fields
from typing import TYPE_CHECKING, Any

from src.domain.validation.interview_step_result_validation_schema import (
    INTERVIEW_STEP_RESULT_VALIDATION_SCHEMA,
)

if TYPE_CHECKING:
    from src.domain.results.interview_step_result import InterviewStepResult


class InterviewStepResultValidator:
    """Validates invariants for InterviewStepResult."""

    @classmethod
    def validate(cls, result: "InterviewStepResult") -> None:
        cls._validate_model_type(result)

        for model_field in fields(result):
            field_name = model_field.name
            value = getattr(result, field_name)
            rules = INTERVIEW_STEP_RESULT_VALIDATION_SCHEMA.get(field_name, {})

            cls._validate_expected_type(
                field_name=field_name,
                value=value,
                expected_type=rules.get("type"),
            )

            if rules.get("non_empty", False):
                cls._validate_non_empty_string(field_name=field_name, value=value)

        cls._validate_question_consistency(result)

    @staticmethod
    def _validate_model_type(result: "InterviewStepResult") -> None:
        from src.domain.results.interview_step_result import InterviewStepResult

        if not isinstance(result, InterviewStepResult):
            raise TypeError("result must be an InterviewStepResult instance")

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
            raise TypeError(f"{field_name} cannot be bool")

        if not isinstance(value, expected_type):
            raise TypeError(f"{field_name} must be a {expected_type} instance")

    @staticmethod
    def _validate_non_empty_string(*, field_name: str, value: object) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field_name} cannot be empty")

    @staticmethod
    def _validate_question_consistency(result: "InterviewStepResult") -> None:
        if result.selection_result.question != result.question:
            raise ValueError("selection_result.question must match question")
