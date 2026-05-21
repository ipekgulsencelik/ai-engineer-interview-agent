from __future__ import annotations

from typing import Any

from src.domain.enums.level import Level
from src.infrastructure.constants.vector_metadata_keys import (
    LEVEL_METADATA_KEY,
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
    ) -> ChromaQueryPayload:
        payload: dict[str, Any] = {
            "query_embeddings": [
                query_embedding,
            ],
            "n_results": top_k,
        }

        if level is not None:
            payload["where"] = {
                LEVEL_METADATA_KEY: level.value,
            }

        return payload