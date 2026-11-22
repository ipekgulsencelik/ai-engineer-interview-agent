"""An embedded SQLite adapter for bounded, auditable question retrieval.

The adapter is an exact cosine-search baseline, not an ANN index. It does not
load plugins, run a database server, execute model repository code, or depend
on the vulnerable ChromaDB package. Keep the dataset bounded and reindex from
trusted Question entities when migrating from Chroma; never read Chroma files.
"""

from __future__ import annotations

import json
import math
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from src.application.ports.question_vector_store import QuestionVectorStore
from src.domain.entities.question import Question
from src.domain.retrieval.question_search_result import QuestionSearchResult
from src.domain.retrieval.search_filters import SearchFilters
from src.domain.retrieval.search_result import SearchResult
from src.infrastructure.errors.vector_store_error import VectorStoreError
from src.infrastructure.vector_stores.sqlite.question_codec import QuestionCodec


class SqliteQuestionVectorStore(QuestionVectorStore):
    """Transactional persistence and exact cosine ranking for a local question bank."""

    MAX_RECORDS = 50_000
    MAX_DIMENSIONS = 4_096

    def __init__(self, *, database_path: str | Path = "data/question_vectors.sqlite3") -> None:
        self.database_path = Path(database_path)
        if str(database_path).strip() in {"", ":memory:"}:
            raise VectorStoreError("A persistent SQLite database path is required.")
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with self._connection() as conn:
                conn.execute(
                    """CREATE TABLE IF NOT EXISTS question_vectors (
                        id TEXT PRIMARY KEY NOT NULL,
                        level TEXT NOT NULL,
                        category TEXT NOT NULL,
                        question_type TEXT NOT NULL,
                        difficulty INTEGER NOT NULL,
                        payload TEXT NOT NULL,
                        embedding TEXT NOT NULL,
                        dimension INTEGER NOT NULL
                    )"""
                )
                conn.execute(
                    "CREATE INDEX IF NOT EXISTS idx_question_vectors_filters "
                    "ON question_vectors (level, category, question_type, difficulty)"
                )
        except sqlite3.Error as exc:
            raise VectorStoreError("Failed to initialize question vector database.") from exc

    @contextmanager
    def _connection(self) -> Iterator[sqlite3.Connection]:
        conn = sqlite3.connect(str(self.database_path), timeout=5.0)
        try:
            conn.execute("PRAGMA trusted_schema=OFF")
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @classmethod
    def _vector(cls, values: list[float], *, name: str) -> list[float]:
        if not isinstance(values, list) or not 1 <= len(values) <= cls.MAX_DIMENSIONS:
            raise VectorStoreError(f"{name} must be a nonempty, bounded list.")
        if any(isinstance(v, bool) or not isinstance(v, (float, int)) for v in values):
            raise VectorStoreError(f"{name} must contain numeric values only.")
        result = [float(v) for v in values]
        if not all(math.isfinite(v) for v in result):
            raise VectorStoreError(f"{name} must contain finite values only.")
        if math.sqrt(sum(v * v for v in result)) == 0.0:
            raise VectorStoreError(f"{name} must have nonzero magnitude.")
        return result

    def index_questions(
        self, *, questions: list[Question], embeddings: list[list[float]]
    ) -> None:
        if not isinstance(questions, list) or not questions:
            raise VectorStoreError("questions must be a nonempty list.")
        if not isinstance(embeddings, list) or len(questions) != len(embeddings):
            raise VectorStoreError("Questions and embeddings count mismatch.")
        if not all(isinstance(q, Question) for q in questions):
            raise VectorStoreError("All questions must be validated Question entities.")
        if len({q.id for q in questions}) != len(questions):
            raise VectorStoreError("Duplicate question IDs in one batch.")
        vectors = [self._vector(value, name="embedding") for value in embeddings]
        dimensions = {len(value) for value in vectors}
        if len(dimensions) != 1:
            raise VectorStoreError("Embedding dimensions differ within batch.")
        try:
            with self._connection() as conn:
                conn.execute("BEGIN IMMEDIATE")
                stored = conn.execute(
                    "SELECT dimension FROM question_vectors LIMIT 1"
                ).fetchone()
                if stored is not None and stored[0] != len(vectors[0]):
                    raise VectorStoreError("Embedding dimension differs from stored index.")
                conn.executemany(
                    """INSERT INTO question_vectors
                    (id, level, category, question_type, difficulty, payload, embedding, dimension)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(id) DO UPDATE SET
                        level=excluded.level, category=excluded.category,
                        question_type=excluded.question_type, difficulty=excluded.difficulty,
                        payload=excluded.payload, embedding=excluded.embedding,
                        dimension=excluded.dimension""",
                    [
                        (
                            question.id,
                            question.level.value,
                            question.category.value,
                            question.question_type.value,
                            question.difficulty,
                            QuestionCodec.encode(question),
                            json.dumps(vector, allow_nan=False),
                            len(vector),
                        )
                        for question, vector in zip(questions, vectors, strict=True)
                    ],
                )
                count = conn.execute("SELECT COUNT(*) FROM question_vectors").fetchone()
                if count is None or count[0] > self.MAX_RECORDS:
                    raise VectorStoreError("Question-vector index capacity exceeded.")
        except sqlite3.Error as exc:
            raise VectorStoreError("Failed to index question vectors.") from exc

    def search_questions(
        self, *, query_embedding: list[float], top_k: int,
        filters: SearchFilters | None = None,
    ) -> list[QuestionSearchResult]:
        vector = self._vector(query_embedding, name="query_embedding")
        if isinstance(top_k, bool) or not isinstance(top_k, int) or top_k < 1:
            raise VectorStoreError("top_k must be a positive integer.")
        if filters is not None and not isinstance(filters, SearchFilters):
            raise VectorStoreError("Invalid search filters.")
        clauses: list[str] = []
        values: list[str | int] = []
        if filters is not None:
            for column, value in (
                ("level", filters.level),
                ("category", filters.category),
                ("question_type", filters.question_type),
            ):
                if value is not None:
                    clauses.append(f"{column} = ?")
                    values.append(value.value)
            if filters.min_difficulty is not None:
                clauses.append("difficulty >= ?")
                values.append(filters.min_difficulty)
            if filters.max_difficulty is not None:
                clauses.append("difficulty <= ?")
                values.append(filters.max_difficulty)
        sql = "SELECT payload, embedding, dimension FROM question_vectors"
        if clauses:
            sql += " WHERE " + " AND ".join(clauses)
        try:
            with self._connection() as conn:
                total = conn.execute("SELECT COUNT(*) FROM question_vectors").fetchone()
                if total is None or total[0] > self.MAX_RECORDS:
                    raise VectorStoreError("Question-vector index capacity exceeded.")
                rows = conn.execute(sql, values).fetchall()
        except sqlite3.Error as exc:
            raise VectorStoreError("Failed to query question vectors.") from exc
        ranked: list[SearchResult] = []
        for payload, raw_embedding, dimension in rows:
            try:
                stored = self._vector(json.loads(raw_embedding), name="stored embedding")
                if dimension != len(vector) or len(stored) != len(vector):
                    raise VectorStoreError("Query/index embedding dimension mismatch.")
                dot = sum(a * b for a, b in zip(vector, stored, strict=True))
                norm_query = math.sqrt(sum(a * a for a in vector))
                norm_stored = math.sqrt(sum(b * b for b in stored))
                similarity = max(-1.0, min(1.0, dot / (norm_query * norm_stored)))
                distance = 1.0 - similarity
                ranked.append(
                    SearchResult(
                        question=QuestionCodec.decode(payload),
                        distance=distance,
                        score=1.0 / (1.0 + distance),
                    )
                )
            except (TypeError, ValueError, OverflowError, ZeroDivisionError) as exc:
                raise VectorStoreError("Invalid persisted question vector.") from exc
        ranked.sort(key=lambda result: (-result.score, result.question.id))
        return ranked[:top_k]

    def count(self) -> int:
        try:
            with self._connection() as conn:
                record = conn.execute("SELECT COUNT(*) FROM question_vectors").fetchone()
                return int(record[0]) if record is not None else 0
        except sqlite3.Error as exc:
            raise VectorStoreError("Failed to count indexed questions.") from exc
