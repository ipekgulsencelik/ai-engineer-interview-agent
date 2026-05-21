from __future__ import annotations

import pytest

from src.domain.entities.question import Question
from src.domain.enums.level import Level
from src.domain.enums.question_category import QuestionCategory
from src.domain.enums.question_type import QuestionType
from src.infrastructure.errors.vector_store_error import (
    VectorStoreError,
)
from src.infrastructure.vector_stores.chroma.chroma_question_vector_store import (
    ChromaQuestionVectorStore,
)


class FakeChromaCollection:
    def __init__(self) -> None:
        self.upsert_payload: dict | None = None
        self.query_payload: dict | None = None

    def upsert(self, **kwargs: object) -> None:
        self.upsert_payload = dict(kwargs)

    def query(self, **kwargs: object) -> dict:
        self.query_payload = dict(kwargs)

        return {
            "ids": [["q1"]],
            "documents": [["What is RAG?"]],
            "metadatas": [
                [
                    {
                        "category": "rag",
                        "level": "JR",
                        "difficulty": 3,
                        "question_type": "conceptual",
                    }
                ]
            ],
            "distances": [[0.12]],
        }


class FailingChromaCollection:
    def upsert(self, **kwargs: object) -> None:
        raise RuntimeError("upsert failed")

    def query(self, **kwargs: object) -> dict:
        raise RuntimeError("query failed")


def _build_question() -> Question:
    return Question(
        id="q1",
        text="What is RAG?",
        category=QuestionCategory.RAG,
        level=Level.JR,
        difficulty=3,
        question_type=QuestionType.CONCEPTUAL,
        expected_points=[
            "retrieval",
            "generation",
        ],
        keywords=[
            "rag",
        ],
        market_weight=0.8,
        followup_allowed=True,
    )


def test_chroma_question_vector_store_should_index_questions() -> None:
    collection = FakeChromaCollection()
    store = ChromaQuestionVectorStore(
        collection=collection,
    )

    question = _build_question()

    store.index_questions(
        questions=[question],
        embeddings=[
            [0.1, 0.2, 0.3],
        ],
    )

    assert collection.upsert_payload is not None
    assert collection.upsert_payload["ids"] == ["q1"]
    assert collection.upsert_payload["documents"] == [
        "What is RAG?",
    ]
    assert collection.upsert_payload["embeddings"] == [
        [0.1, 0.2, 0.3],
    ]


def test_chroma_question_vector_store_should_add_single_question() -> None:
    collection = FakeChromaCollection()
    store = ChromaQuestionVectorStore(
        collection=collection,
    )

    store.add_question(
        question=_build_question(),
        embedding=[0.1, 0.2, 0.3],
    )

    assert collection.upsert_payload is not None
    assert collection.upsert_payload["ids"] == ["q1"]


def test_chroma_question_vector_store_should_search_questions() -> None:
    collection = FakeChromaCollection()
    store = ChromaQuestionVectorStore(
        collection=collection,
    )

    results = store.search_questions(
        query_embedding=[0.1, 0.2, 0.3],
        top_k=1,
        level=Level.JR,
    )

    assert collection.query_payload is not None
    assert collection.query_payload["n_results"] == 1
    assert collection.query_payload["where"] == {
        "level": "JR",
    }
    assert len(results) == 1


def test_chroma_question_vector_store_should_fail_when_index_input_lengths_mismatch() -> None:
    collection = FakeChromaCollection()
    store = ChromaQuestionVectorStore(
        collection=collection,
    )

    with pytest.raises(VectorStoreError):
        store.index_questions(
            questions=[
                _build_question(),
            ],
            embeddings=[],
        )


def test_chroma_question_vector_store_should_wrap_upsert_error() -> None:
    store = ChromaQuestionVectorStore(
        collection=FailingChromaCollection(),
    )

    with pytest.raises(VectorStoreError):
        store.index_questions(
            questions=[
                _build_question(),
            ],
            embeddings=[
                [0.1, 0.2, 0.3],
            ],
        )


def test_chroma_question_vector_store_should_wrap_query_error() -> None:
    store = ChromaQuestionVectorStore(
        collection=FailingChromaCollection(),
    )

    with pytest.raises(VectorStoreError):
        store.search_questions(
            query_embedding=[0.1, 0.2, 0.3],
            top_k=1,
            level=Level.JR,
        )