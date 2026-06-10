from __future__ import annotations

from src.domain.retrieval.search_filters import (
    SearchFilters,
)
from src.infrastructure.constants.chroma_filter_operators import (
    CHROMA_GTE_OPERATOR,
    CHROMA_LTE_OPERATOR,
)
from src.infrastructure.constants.vector_metadata_keys import (
    CATEGORY_METADATA_KEY,
    DIFFICULTY_METADATA_KEY,
    LEVEL_METADATA_KEY,
    QUESTION_TYPE_METADATA_KEY,
)
from src.infrastructure.vector_stores.chroma.chroma_question_types import (
    ChromaWhereFilter,
)


class ChromaFilterBuilder:
    """
    Chroma metadata filter query builder.
    """

    @classmethod
    def build(
        cls,
        *,
        filters: SearchFilters | None,
    ) -> ChromaWhereFilter | None:
        if filters is None:
            return None

        where: ChromaWhereFilter = {}

        cls._add_category_filter(
            where=where,
            filters=filters,
        )

        cls._add_level_filter(
            where=where,
            filters=filters,
        )

        cls._add_question_type_filter(
            where=where,
            filters=filters,
        )

        cls._add_difficulty_filters(
            where=where,
            filters=filters,
        )

        return where or None

    @staticmethod
    def _add_category_filter(
        *,
        where: ChromaWhereFilter,
        filters: SearchFilters,
    ) -> None:
        if filters.category is not None:
            where[CATEGORY_METADATA_KEY] = (
                filters.category.value
            )

    @staticmethod
    def _add_level_filter(
        *,
        where: ChromaWhereFilter,
        filters: SearchFilters,
    ) -> None:
        if filters.level is not None:
            where[LEVEL_METADATA_KEY] = (
                filters.level.value
            )

    @staticmethod
    def _add_question_type_filter(
        *,
        where: ChromaWhereFilter,
        filters: SearchFilters,
    ) -> None:
        if filters.question_type is not None:
            where[QUESTION_TYPE_METADATA_KEY] = (
                filters.question_type.value
            )

    @staticmethod
    def _add_difficulty_filters(
        *,
        where: ChromaWhereFilter,
        filters: SearchFilters,
    ) -> None:
        difficulty_conditions: dict[str, int] = {}

        if filters.min_difficulty is not None:
            difficulty_conditions[
                CHROMA_GTE_OPERATOR
            ] = filters.min_difficulty

        if filters.max_difficulty is not None:
            difficulty_conditions[
                CHROMA_LTE_OPERATOR
            ] = filters.max_difficulty

        if difficulty_conditions:
            where[DIFFICULTY_METADATA_KEY] = (
                difficulty_conditions
            )