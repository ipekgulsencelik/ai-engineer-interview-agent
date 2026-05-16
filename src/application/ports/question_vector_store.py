from __future__ import annotations

from typing import Protocol, runtime_checkable

from src.domain.entities.question import Question


@runtime_checkable
class QuestionVectorStore(Protocol):
    """
    Question-specific vector store port.
    """

    def index_questions(
        self,
        *,
        questions: list[Question],
        embeddings: list[list[float]],
    ) -> None:
        ...

    def search_questions(
        self,
        *,
        query_embedding: list[float],
        top_k: int,
    ) -> list[Question]:
        ...