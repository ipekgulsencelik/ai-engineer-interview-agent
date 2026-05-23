from __future__ import annotations

import math
from dataclasses import fields
from datetime import datetime

from src.domain.results.selection_result import (
    SelectionResult,
)
from src.domain.validation.schema_types import (
    ValidationRule,
)
from src.domain.validation.selection_result_validation_schema import (
    SELECTION_RESULT_VALIDATION_SCHEMA,
)


class SelectionResultValidator:
    """
    SelectionResult invariant validator.
    """

    @classmethod
    def validate(
        cls,
        result: SelectionResult,
    ) -> None:
        cls._validate_model_type(
            result,
        )

        for model_field in fields(result):
            field_name = model_field.name
            value = getattr(
                result,
                field_name,
            )

            rules = SELECTION_RESULT_VALIDATION_SCHEMA[
                field_name
            ]

            cls._validate_nullable(
                field_name=field_name,
                value=value,
                nullable=rules.get(
                    "nullable",
                    False,
                ),
            )

            if value is None:
                continue

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

            cls._validate_timezone_aware(
                field_name=field_name,
                value=value,
                rules=rules,
            )

        cls._validate_rank_candidate_consistency(
            result,
        )

    @staticmethod
    def _validate_model_type(
        result: object,
    ) -> None:
        if not isinstance(
            result,
            SelectionResult,
        ):
            raise TypeError(
                "result must be SelectionResult."
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
    def _validate_finite(
        *,
        field_name: str,
        value: object,
        rules: ValidationRule,
    ) -> None:
        if rules.get("finite") is not True:
            return

        if not math.isfinite(
            float(value),
        ):
            raise ValueError(
                f"{field_name} must be finite."
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
    def _validate_timezone_aware(
        *,
        field_name: str,
        value: object,
        rules: ValidationRule,
    ) -> None:
        if rules.get("timezone_aware") is not True:
            return

        if not isinstance(
            value,
            datetime,
        ):
            raise TypeError(
                f"{field_name} must be datetime."
            )

        if (
            value.tzinfo is None
            or value.utcoffset() is None
        ):
            raise ValueError(
                f"{field_name} must be timezone-aware."
            )

    @staticmethod
    def _validate_rank_candidate_consistency(
        result: SelectionResult,
    ) -> None:
        if (
            result.rank is not None
            and result.candidate_count is not None
            and result.rank > result.candidate_count
        ):
            raise ValueError(
                "rank cannot be greater than candidate_count."
            )