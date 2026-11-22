"""Real, dependency-free tests for the ChromaDB-free question vector adapter."""

from __future__ import annotations

import json
import sqlite3

import pytest

from src.domain.entities.question import Question
from src.domain.enums.level import Level
from src.domain.enums.question_category import QuestionCategory
from src.domain.enums.question_type import QuestionType
from src.domain.retrieval.search_filters import SearchFilters
from src.infrastructure.errors.vector_store_error import VectorStoreError
from src.infrastructure.vector_stores.sqlite.sqlite_question_vector_store import (
    SqliteQuestionVectorStore,
)


def question(identifier: str, level: Level = Level.MID) -> Question:
    return Question(
        id=identifier,
        text=f"Question about RAG {identifier}",
        level=level,
        category=QuestionCategory.RAG,
        question_type=QuestionType.CONCEPTUAL,
        difficulty=2,
        expected_points=["Retrieval"],
        keywords=["RAG", identifier],
        followup="Explain your reasoning.",
    )


def test_persistent_round_trip_and_complete_question_metadata(tmp_path) -> None:
    path = tmp_path / "index.sqlite3"
    store = SqliteQuestionVectorStore(database_path=path)
    store.index_questions(questions=[question("a")], embeddings=[[1.0, 0.0]])
    reloaded = SqliteQuestionVectorStore(database_path=path)
    result = reloaded.search_questions(query_embedding=[1.0, 0.0], top_k=5)
    assert reloaded.count() == 1
    assert len(result) == 1
    assert result[0].question == question("a")
    assert result[0].distance == pytest.approx(0.0)
    assert result[0].score == pytest.approx(1.0)


def test_rank_filter_and_deterministic_tie_breaking(tmp_path) -> None:
    store = SqliteQuestionVectorStore(database_path=tmp_path / "index.sqlite3")
    store.index_questions(
        questions=[question("z"), question("a"), question("senior", Level.SENIOR)],
        embeddings=[[1.0, 0.0], [1.0, 0.0], [0.0, 1.0]],
    )
    results = store.search_questions(
        query_embedding=[1.0, 0.0],
        top_k=2,
        filters=SearchFilters(level=Level.MID, category=QuestionCategory.RAG),
    )
    assert [result.question.id for result in results] == ["a", "z"]
    assert store.search_questions(
        query_embedding=[1.0, 0.0], top_k=5,
        filters=SearchFilters(level=Level.JR),
    ) == []


def test_atomic_upsert_and_reindex_idempotency(tmp_path) -> None:
    store = SqliteQuestionVectorStore(database_path=tmp_path / "index.sqlite3")
    store.index_questions(questions=[question("a")], embeddings=[[1.0, 0.0]])
    store.index_questions(questions=[question("a")], embeddings=[[0.0, 1.0]])
    assert store.count() == 1
    assert store.search_questions(query_embedding=[0.0, 1.0], top_k=1)[0].score == pytest.approx(1.0)


@pytest.mark.parametrize("embedding", [[float("nan"), 1.0], [0.0, 0.0], [True, 1.0], [], [float("inf"), 1.0]])
def test_rejects_bad_embeddings_without_writing(tmp_path, embedding) -> None:
    store = SqliteQuestionVectorStore(database_path=tmp_path / "index.sqlite3")
    with pytest.raises(VectorStoreError):
        store.index_questions(questions=[question("a")], embeddings=[embedding])
    assert store.count() == 0


def test_rejects_mixed_dimensions_and_duplicate_ids(tmp_path) -> None:
    store = SqliteQuestionVectorStore(database_path=tmp_path / "index.sqlite3")
    with pytest.raises(VectorStoreError):
        store.index_questions(
            questions=[question("a"), question("b")], embeddings=[[1.0], [1.0, 2.0]]
        )
    with pytest.raises(VectorStoreError):
        store.index_questions(
            questions=[question("a"), question("a")], embeddings=[[1.0], [1.0]]
        )
    assert store.count() == 0


def test_dimension_mismatch_rejected_for_existing_index_and_query(tmp_path) -> None:
    store = SqliteQuestionVectorStore(database_path=tmp_path / "index.sqlite3")
    store.index_questions(questions=[question("a")], embeddings=[[1.0, 0.0]])
    with pytest.raises(VectorStoreError):
        store.index_questions(questions=[question("b")], embeddings=[[1.0, 0.0, 0.0]])
    with pytest.raises(VectorStoreError):
        store.search_questions(query_embedding=[1.0, 0.0, 0.0], top_k=1)
    assert store.count() == 1


def test_tampered_persisted_embedding_fails_closed(tmp_path) -> None:
    path = tmp_path / "index.sqlite3"
    store = SqliteQuestionVectorStore(database_path=path)
    store.index_questions(questions=[question("a")], embeddings=[[1.0, 0.0]])
    with sqlite3.connect(str(path)) as conn:
        conn.execute(
            "UPDATE question_vectors SET embedding=? WHERE id=?",
            (json.dumps([float("nan"), 0.0]), "a"),
        )
    with pytest.raises(VectorStoreError):
        store.search_questions(query_embedding=[1.0, 0.0], top_k=1)


def test_sql_metacharacters_are_data_not_queries(tmp_path) -> None:
    store = SqliteQuestionVectorStore(database_path=tmp_path / "index.sqlite3")
    identifier = "abc'); DROP TABLE question_vectors; --"
    store.index_questions(questions=[question(identifier)], embeddings=[[1.0]])
    assert store.count() == 1
    assert store.search_questions(query_embedding=[1.0], top_k=1)[0].question.id == identifier


def test_empty_index_and_invalid_k(tmp_path) -> None:
    store = SqliteQuestionVectorStore(database_path=tmp_path / "index.sqlite3")
    assert store.search_questions(query_embedding=[1.0], top_k=1) == []
    with pytest.raises(VectorStoreError):
        store.search_questions(query_embedding=[1.0], top_k=0)
    with pytest.raises(VectorStoreError):
        store.search_questions(query_embedding=[1.0], top_k=True)
