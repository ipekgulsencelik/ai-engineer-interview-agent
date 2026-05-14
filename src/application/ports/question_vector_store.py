from __future__ import annotations

from typing import Protocol, runtime_checkable

from src.domain.entities.question import Question
from src.domain.enums.level import Level


@runtime_checkable
class QuestionVectorStore(Protocol):
    """Port contract for retrieving interview questions via vector search."""

    def search_questions(
        self,
        *,
        embedding: list[float],
        top_k: int,
        level: Level,
    ) -> list[Question]:
        ...