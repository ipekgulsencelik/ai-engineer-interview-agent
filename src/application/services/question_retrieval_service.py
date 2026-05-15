from __future__ import annotations

from src.domain.scoring.scoring_context import ScoringContext


class QuestionRetrievalService:
    """
    Semantic question retrieval application service.

    Embedding provider ve vector store adapter'larını kullanarak
    query/context'e uygun candidate question listesini getirir.
    """

    def __init__(
        self,
        *,
        embedding_provider,
        vector_store,
    ) -> None:
        self._embedding_provider = embedding_provider
        self._vector_store = vector_store

    def retrieve(
        self,
        *,
        query: str,
        context: ScoringContext,
        top_k: int = 5,
    ):
        embedding = self._embedding_provider.embed_query(
            query,
        )

        return self._vector_store.search(
            query_embedding=embedding,
            context=context,
            top_k=top_k,
        )