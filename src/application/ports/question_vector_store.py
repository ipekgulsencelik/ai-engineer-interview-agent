from __future__ import annotations

from typing import Protocol, runtime_checkable

from src.domain.entities.question import Question
from src.domain.retrieval.question_search_result import (
    QuestionSearchResult,
)
from src.domain.value_objects.search_filters import (
    SearchFilters,
)


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
        filters: SearchFilters | None = None,
    ) -> list[QuestionSearchResult]:
        ...