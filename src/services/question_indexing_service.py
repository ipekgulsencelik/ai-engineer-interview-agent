from __future__ import annotations

from src.application.ports.embedding_provider import EmbeddingProvider
from src.application.ports.vector_store import VectorStore
from src.application.validators.question_indexing_service_validator import (
    QuestionIndexingServiceValidator,
)
from src.domain.entities.question import Question


class QuestionIndexingService:
    """Question indexing orchestration service."""

    def __init__(
        self,
        *,
        embedding_provider: EmbeddingProvider,
        vector_store: VectorStore,
    ) -> None:
        QuestionIndexingServiceValidator.validate_dependencies(
            embedding_provider=embedding_provider,
            vector_store=vector_store,
        )

        self._embedding_provider = embedding_provider
        self._vector_store = vector_store

    def index_questions(
        self,
        *,
        questions: list[Question],
    ) -> None:
        QuestionIndexingServiceValidator.validate_questions(
            questions,
        )

        for question in questions:
            document = self._build_document(
                question,
            )

            embedding = self._embedding_provider.embed_text(
                document,
            )

            self._vector_store.add(
                id=question.id,
                text=document,
                embedding=embedding,
                metadata=self._build_metadata(question),
            )

    @staticmethod
    def _build_document(
        question: Question,
    ) -> str:
        parts: list[str] = [
            question.text,
        ]

        if question.keywords:
            parts.extend(
                question.keywords,
            )

        if question.expected_points:
            parts.extend(
                question.expected_points,
            )

        return " ".join(parts)

    @staticmethod
    def _build_metadata(question: Question) -> dict[str, str]:
        return {
            "category": str(question.category),
            "level": str(question.level),
            "question_type": str(question.question_type),
            "difficulty": str(question.difficulty),
            "followup_allowed": str(question.followup_allowed),
        }