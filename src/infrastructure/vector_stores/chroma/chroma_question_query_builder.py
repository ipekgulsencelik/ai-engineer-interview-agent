from __future__ import annotations

from src.domain.enums.level import Level
from src.infrastructure.vector_stores.chroma.chroma_question_types import (
    ChromaQueryPayload,
)


class ChromaQuestionQueryBuilder:
    """Builds ChromaDB query payloads for question retrieval."""

    @staticmethod
    def build(*, embedding: list[float], top_k: int, level: Level) -> ChromaQueryPayload:
        return {
            "query_embeddings": [embedding],
            "n_results": top_k,
            "where": {"level": level.value},
        }