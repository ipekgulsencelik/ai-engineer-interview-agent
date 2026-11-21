from __future__ import annotations

from typing import TYPE_CHECKING

from src.domain.schemas.search_filters_schema import (
    SEARCH_FILTERS_SCHEMA,
)
from src.domain.validators.schema_validator import (
    SchemaValidator,
)

if TYPE_CHECKING:
    from src.domain.retrieval.search_filters import SearchFilters


class SearchFiltersValidator:
    """
    SearchFilters invariant validator.
    """

    @classmethod
    def validate(
        cls,
        filters: SearchFilters,
    ) -> None:
        """
        Validate SearchFilters invariants.
        """

        SchemaValidator.validate_object(
            obj=filters,
            schema=SEARCH_FILTERS_SCHEMA,
        )

        cls._validate_difficulty_range(
            filters=filters,
        )

    @staticmethod
    def _validate_difficulty_range(
        *,
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