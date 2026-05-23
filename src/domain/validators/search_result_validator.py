from __future__ import annotations

from dataclasses import fields
from typing import TYPE_CHECKING

from src.domain.validation.search_result_validation_schema import (
    SEARCH_RESULT_VALIDATION_SCHEMA,
)
from src.domain.validators.base_schema_validator import BaseSchemaValidator

if TYPE_CHECKING:
    from src.domain.retrieval.search_result import SearchResult


class SearchResultValidator:
    """
    SearchResult invariant validator.
    """

    @classmethod
    def validate(
        cls,
        result: SearchResult,
    ) -> None:
        from src.domain.retrieval.search_result import (
            SearchResult as SearchResultModel,
        )

        BaseSchemaValidator.validate_model_type(
            value=result,
            expected_type=SearchResultModel,
            field_name="result",
        )

        for model_field in fields(result):
            field_name = model_field.name
            value = getattr(result, field_name)
            rules = SEARCH_RESULT_VALIDATION_SCHEMA[field_name]

            BaseSchemaValidator.validate_nullable(
                field_name=field_name,
                value=value,
                rules=rules,
            )

            if value is None:
                continue

            BaseSchemaValidator.validate_type(
                field_name=field_name,
                value=value,
                rules=rules,
            )

            BaseSchemaValidator.validate_numeric_bounds(
                field_name=field_name,
                value=value,
                rules=rules,
            )
