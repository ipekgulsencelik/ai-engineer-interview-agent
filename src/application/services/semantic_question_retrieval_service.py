from __future__ import annotations

from src.application.ports.embedding_provider import (
    EmbeddingProvider,
)
from src.application.ports.question_vector_store import (
    QuestionVectorStore,
)
from src.application.builders.search_filters_builder import (
    SearchFiltersBuilder,
)
from src.domain.retrieval.question_search_result import (
    QuestionSearchResult,
)
from src.domain.scoring.scoring_context import (
    ScoringContext,
)


class SemanticQuestionRetrievalService:
    """
    Interview-aware semantic question retrieval
    application service.

    Bu servis:
        - query text'ini embedding'e çevirir
        - ScoringContext'ten retrieval filter üretir
        - QuestionVectorStore üzerinden semantic
          search çalıştırır
        - QuestionSearchResult listesi döndürür

    Business ranking, final selection veya
    scoring yapmaz.
    """

    def __init__(
        self,
        *,
        embedding_provider: EmbeddingProvider,
        vector_store: QuestionVectorStore,
    ) -> None:
        self._embedding_provider = (
            embedding_provider
        )

        self._vector_store = vector_store

    def retrieve(
        self,
        *,
        query: str,
        context: ScoringContext,
        top_k: int = 5,
    ) -> list[QuestionSearchResult]:
        query_embedding = (
            self._embedding_provider.embed_text(
                text=query,
            )
        )

        filters = SearchFiltersBuilder.build(
            context=context,
        )

        return self._vector_store.search_questions(
            query_embedding=query_embedding,
            top_k=top_k,
            filters=filters,
        )