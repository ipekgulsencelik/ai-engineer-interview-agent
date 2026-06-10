from __future__ import annotations

from src.application.ports.embedding_provider import EmbeddingProvider
from src.application.ports.vector_store import VectorStore
from src.domain.repositories.question_repository import QuestionRepository
from src.domain.scoring.scoring_context import ScoringContext


class QuestionRetrievalServiceValidator:

    @staticmethod
    def validate_dependencies(
        *,
        embedding_provider: EmbeddingProvider,
        vector_store: VectorStore,
        repository: QuestionRepository,
    ) -> None:
        if embedding_provider is None:
            raise ValueError("embedding_provider cannot be None")
        if vector_store is None:
            raise ValueError("vector_store cannot be None")
        if repository is None:
            raise ValueError("repository cannot be None")

        if not isinstance(embedding_provider, EmbeddingProvider):
            raise TypeError("embedding_provider must be EmbeddingProvider")
        if not isinstance(vector_store, VectorStore):
            raise TypeError("vector_store must be VectorStore")
        if not isinstance(repository, QuestionRepository):
            raise TypeError("repository must be QuestionRepository")


    @staticmethod
    def validate_query(query: str) -> str:
        if not isinstance(query, str):
            raise TypeError(
                "query must be a string."
            )

        normalized = query.strip()

        if not normalized:
            raise ValueError("query cannot be empty")

        return normalized


    @staticmethod
    def validate_context(context: ScoringContext) -> None:
        if not isinstance(context, ScoringContext):
            raise TypeError("context must be a ScoringContext instance")

    @staticmethod
    def validate_top_k(top_k: int) -> None:
        if not isinstance(top_k, int):
            raise TypeError("top_k must be int")
        if top_k <= 0:
            raise ValueError("top_k must be greater than 0")

    @staticmethod
    def validate_limit(limit: int) -> None:
        QuestionRetrievalServiceValidator.validate_top_k(limit)