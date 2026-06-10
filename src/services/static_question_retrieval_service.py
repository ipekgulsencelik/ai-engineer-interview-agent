from __future__ import annotations

from src.application.ports.embedding_provider import EmbeddingProvider
from src.application.ports.vector_store import VectorStore
from src.application.validators.question_retrieval_service_validator import (
    QuestionRetrievalServiceValidator,
)
from src.domain.entities.question import Question
from src.domain.repositories.question_repository import QuestionRepository
from src.domain.scoring.scoring_context import ScoringContext


class StaticQuestionRetrievalService:
    """Static question retrieval orchestration service."""

    def __init__(
        self,
        *,
        embedding_provider: EmbeddingProvider,
        vector_store: VectorStore,
        repository: QuestionRepository,
    ) -> None:
        QuestionRetrievalServiceValidator.validate_dependencies(
            embedding_provider=embedding_provider,
            vector_store=vector_store,
            repository=repository,
        )
        
        self._embedding_provider = embedding_provider
        self._vector_store = vector_store
        self._repository = repository

    def retrieve(
        self,
        *,
        query: str,
        context: ScoringContext,
        top_k: int = 5,
    ) -> list[Question]:
        normalized_query = QuestionRetrievalServiceValidator.validate_query(query)
        QuestionRetrievalServiceValidator.validate_context(context)
        QuestionRetrievalServiceValidator.validate_top_k(top_k)

        embedding = self._embedding_provider.embed_text(normalized_query)
        results = self._vector_store.search(
            query_embedding=embedding,
            limit=top_k,
            where={"level": str(context.current_level)},
        )

        questions: list[Question] = []
        for result in results:
            question = self._repository.get_by_id(result.id)
            if question is not None:
                questions.append(question)
        return questions