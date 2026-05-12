from __future__ import annotations

import math
from dataclasses import fields
from datetime import datetime
from typing import TYPE_CHECKING, Any

from src.domain.validation.selection_result_validation_schema import (
    SELECTION_RESULT_VALIDATION_SCHEMA,
)

if TYPE_CHECKING:
    from src.domain.results.selection_result import SelectionResult


class SelectionResultValidator:
    @classmethod
    def validate(
        cls,
        result: "SelectionResult",
    ) -> None:
        cls._validate_model_type(result)

        for model_field in fields(result):
            field_name = model_field.name
            value = getattr(result, field_name)

            rules = SELECTION_RESULT_VALIDATION_SCHEMA.get(field_name, {})

            nullable = rules.get("nullable", False)

            if value is None:
                if nullable:
                    continue

                raise TypeError(f"{field_name} cannot be None.")

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

            if rules.get("timezone_aware", False):
                cls._validate_timezone_aware_datetime(
                    field_name=field_name,
                    value=value,
                )

            if "min_value" in rules:
                cls._validate_min_value(
                    field_name=field_name,
                    value=value,
                    min_value=rules["min_value"],
                )

        cls._validate_rank_candidate_relation(
            rank=result.rank,
            candidate_count=result.candidate_count,
        )

    @staticmethod
    def _validate_model_type(
        result: "SelectionResult",
    ) -> None:
        from src.domain.results.selection_result import SelectionResult

        if not isinstance(result, SelectionResult):
            raise TypeError("result must be a SelectionResult instance.")

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
    def _validate_timezone_aware_datetime(
        *,
        field_name: str,
        value: datetime,
    ) -> None:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError(f"{field_name} must be timezone-aware.")

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
    def _validate_rank_candidate_relation(
        *,
        rank: int | None,
        candidate_count: int | None,
    ) -> None:
        if rank is None or candidate_count is None:
            return

        if rank > candidate_count:
            raise ValueError(
                "rank cannot be greater than candidate_count."
            )