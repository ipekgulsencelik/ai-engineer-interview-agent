from __future__ import annotations

import math
from dataclasses import fields, is_dataclass
from typing import TYPE_CHECKING, Any

from src.domain.validation.search_result_validation_schema import (
    SEARCH_RESULT_VALIDATION_SCHEMA,
)

if TYPE_CHECKING:
    from src.domain.retrieval.search_result import SearchResult


class SearchResultValidator:
    """
    SearchResult domain snapshot invariant validator.
    """

    @classmethod
    def validate(
        cls,
        result: "SearchResult",
    ) -> None:
        cls._validate_model_type(result)

        for model_field in fields(result):
            field_name = model_field.name
            value = getattr(result, field_name)

            rules = SEARCH_RESULT_VALIDATION_SCHEMA.get(
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
                reject_bool=rules.get("reject_bool", False),
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
        result: "SearchResult",
    ) -> None:
        from src.domain.retrieval.search_result import SearchResult

        if not isinstance(result, SearchResult):
            raise TypeError(
                "result must be a SearchResult instance."
            )

        if not is_dataclass(result):
            raise TypeError(
                "result must be a dataclass instance."
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
        reject_bool: bool,
    ) -> None:
        if expected_type is None:
            return

        if reject_bool and isinstance(value, bool):
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
        value: object,
    ) -> None:
        if not isinstance(value, (int, float)):
            raise TypeError(
                f"{field_name} must be numeric."
            )

        if not math.isfinite(float(value)):
            raise ValueError(
                f"{field_name} must be finite."
            )

    @staticmethod
    def _validate_min_value(
        *,
        field_name: str,
        value: object,
        min_value: float,
    ) -> None:
        if float(value) < min_value:
            raise ValueError(
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
        if float(value) > max_value:
            raise ValueError(
                f"{field_name} must be less than or equal to "
                f"{max_value}."
            )