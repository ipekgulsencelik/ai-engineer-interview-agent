from dataclasses import dataclass

import pytest

from src.domain.entities.question import Question
from src.domain.enums.level import Level
from src.domain.enums.question_category import QuestionCategory
from src.domain.enums.question_type import QuestionType
from src.domain.repositories.question_repository import QuestionRepository
from src.domain.scoring.scoring_context import ScoringContext
from src.domain.search.search_result import SearchResult
from src.services.question_retrieval_service import QuestionRetrievalService


@dataclass
class FakeEmbeddingProvider:
    def embed_text(self, text: str) -> list[float]:
        return [float(len(text))]


@dataclass
class FakeVectorStore:
    results: list[SearchResult]

    def add(self, *, id: str, text: str, embedding: list[float], metadata: dict[str, str]) -> None:
        return None

    def add_many(
        self,
        *,
        ids: list[str],
        texts: list[str],
        embeddings: list[list[float]],
        metadatas: list[dict[str, str]],
    ) -> None:
        return None

    def search(
        self,
        *,
        query_embedding: list[float],
        limit: int = 5,
        where: dict | None = None,
    ) -> list[SearchResult]:
        return self.results[:limit]

    def count(self) -> int:
        return len(self.results)


class FakeQuestionRepository(QuestionRepository):
    def __init__(self, questions: list[Question]) -> None:
        self._questions = questions

    def list_all(self) -> list[Question]:
        return self._questions

    def get_by_id(self, question_id: str) -> Question | None:
        return next((q for q in self._questions if q.id == question_id), None)


def build_question(question_id: str, text: str) -> Question:
    return Question(
        id=question_id,
        text=text,
        category=QuestionCategory.RAG,
        level=Level.MID,
        difficulty=2,
        question_type=QuestionType.CONCEPTUAL,
        expected_points=["point"],
        keywords=["kw"],
    )


def build_context() -> ScoringContext:
    return ScoringContext(current_level=Level.MID)


def test_retrieve_returns_questions() -> None:
    questions = [build_question("q1", "text one")]
    results = [SearchResult(id="q1", text="text one", score=0.1, metadata={})]

    service = QuestionRetrievalService(
        embedding_provider=FakeEmbeddingProvider(),
        vector_store=FakeVectorStore(results=results),
        repository=FakeQuestionRepository(questions),
    )

    retrieved = service.retrieve(query="rag", context=build_context(), top_k=1)

    assert [q.id for q in retrieved] == ["q1"]


def test_retrieve_rejects_empty_query() -> None:
    service = QuestionRetrievalService(
        embedding_provider=FakeEmbeddingProvider(),
        vector_store=FakeVectorStore(results=[]),
        repository=FakeQuestionRepository([]),
    )

    with pytest.raises(ValueError, match="query cannot be empty"):
        service.retrieve(query="   ", context=build_context())


def test_retrieve_rejects_non_positive_top_k() -> None:
    service = QuestionRetrievalService(
        embedding_provider=FakeEmbeddingProvider(),
        vector_store=FakeVectorStore(results=[]),
        repository=FakeQuestionRepository([]),
    )

    with pytest.raises(ValueError, match="top_k must be greater than 0"):
        service.retrieve(query="rag", context=build_context(), top_k=0)