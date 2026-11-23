from __future__ import annotations

from typing import Any

from src.domain.enums.level import Level
from src.domain.retrieval.search_filters import SearchFilters
from src.infrastructure.vector_stores.chroma.chroma_filter_builder import (
    ChromaFilterBuilder,
)
from src.infrastructure.vector_stores.chroma.chroma_question_types import (
    ChromaQueryPayload,
)


class ChromaQuestionQueryBuilder:
    """
    ChromaDB question search query payload builder.
    """

    @staticmethod
    def build(
        *,
        query_embedding: list[float],
        top_k: int,
        level: Level | None = None,
        filters: SearchFilters | None = None,
    ) -> ChromaQueryPayload:
        payload: dict[str, Any] = {
            "query_embeddings": [
                query_embedding,
            ],
            "n_results": top_k,
        }

        if filters is None and level is not None:
            filters = SearchFilters(level=level)

        where = ChromaFilterBuilder.build(filters=filters)
        if where is not None:
            payload["where"] = where

        return payload