from __future__ import annotations

from dataclasses import fields

from src.domain.retrieval.search_filters import SearchFilters
from src.domain.validation.search_filters_validation_schema import (
    SEARCH_FILTERS_VALIDATION_SCHEMA,
)


class SearchFiltersValidator:
    """
    SearchFilters invariant validator.
    """

    @classmethod
    def validate(
        cls,
        filters: SearchFilters,
    ) -> None:
        for model_field in fields(filters):
            field_name = model_field.name
            value = getattr(filters, field_name)
            rules = SEARCH_FILTERS_VALIDATION_SCHEMA[field_name]

            cls._validate_nullable(
                field_name=field_name,
                value=value,
                nullable=rules.get("nullable", False),
            )

            if value is None:
                continue

            cls._validate_type(
                field_name=field_name,
                value=value,
                rules=rules,
            )

            cls._validate_min_max(
                field_name=field_name,
                value=value,
                rules=rules,
            )

        cls._validate_difficulty_range(filters)

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
        rules: dict,
    ) -> None:
        if rules.get("reject_bool") is True and isinstance(value, bool):
            raise TypeError(
                f"{field_name} cannot be bool."
            )

        expected_type = rules.get("type")

        if expected_type is not None and not isinstance(value, expected_type):
            raise TypeError(
                f"{field_name} has invalid type."
            )

    @staticmethod
    def _validate_min_max(
        *,
        field_name: str,
        value: object,
        rules: dict,
    ) -> None:
        min_value = rules.get("min_value")
        max_value = rules.get("max_value")

        if min_value is not None and value < min_value:
            raise ValueError(
                f"{field_name} must be >= {min_value}."
            )

        if max_value is not None and value > max_value:
            raise ValueError(
                f"{field_name} must be <= {max_value}."
            )

    @staticmethod
    def _validate_difficulty_range(
        filters: SearchFilters,
    ) -> None:
        if (
            filters.min_difficulty is not None
            and filters.max_difficulty is not None
            and filters.min_difficulty > filters.max_difficulty
        ):
            raise ValueError(
                "min_difficulty cannot exceed max_difficulty."
            )