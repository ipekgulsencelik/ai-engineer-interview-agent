from __future__ import annotations

from src.application.ports.embedding_provider import (
    EmbeddingProvider,
)
from src.application.ports.question_vector_store import (
    QuestionVectorStore,
)
from src.domain.entities.question import Question


class QuestionIndexingService:
    """
    Question embedding indexing orchestration.
    """

    def __init__(
        self,
        *,
        embedding_provider: EmbeddingProvider,
        vector_store: QuestionVectorStore,
    ) -> None:
        self._embedding_provider = embedding_provider
        self._vector_store = vector_store

    def index_questions(
        self,
        *,
        questions: list[Question],
    ) -> None:
        texts = [
            question.text
            for question in questions
        ]

        embeddings = self._embedding_provider.embed_many(
            texts=texts,
        )

        self._vector_store.index_questions(
            questions=questions,
            embeddings=embeddings,
        )