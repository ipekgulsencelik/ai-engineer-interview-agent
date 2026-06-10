from __future__ import annotations

from src.application.ports.embedding_provider import EmbeddingProvider
from src.application.ports.vector_store import VectorStore
from src.application.validation.question_indexing_validation_schema import (
    QUESTION_INDEXING_VALIDATION_SCHEMA,
)
from src.domain.entities.question import Question


class QuestionIndexingServiceValidator:

    @staticmethod
    def validate_dependencies(
        *,
        embedding_provider: EmbeddingProvider,
        vector_store: VectorStore,
    ) -> None:
        if embedding_provider is None:
            raise ValueError("embedding_provider cannot be None")
        if vector_store is None:
            raise ValueError("vector_store cannot be None")

        if not isinstance(embedding_provider, EmbeddingProvider):
            raise TypeError("embedding_provider must be EmbeddingProvider")
        if not isinstance(vector_store, VectorStore):
            raise TypeError("vector_store must be VectorStore")

    @staticmethod
    def validate_questions(questions: list[Question]) -> None:
        rules = QUESTION_INDEXING_VALIDATION_SCHEMA["questions"]

        collection_type = rules["collection_type"]
        if not isinstance(questions, collection_type):
            raise TypeError("questions must be list[Question]")

        if rules.get("non_empty", False) and not questions:
            raise ValueError("questions cannot be empty")

        item_type = rules["item_type"]
        for question in questions:
            if not isinstance(question, item_type):
                raise TypeError("all questions must be Question instances")