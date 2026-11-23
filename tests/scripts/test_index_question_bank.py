"""End-to-end check of the question indexing script against a real Chroma store.

Uses a deterministic offline embedder so the test needs no model download,
but exercises the real repository, mapper, indexing service and Chroma adapter.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

pytest.importorskip("chromadb")

from src.domain.enums.level import Level  # noqa: E402
from src.domain.retrieval.search_filters import SearchFilters  # noqa: E402
from src.infrastructure.vector_stores.chroma.chroma_client_factory import (  # noqa: E402
    create_chroma_client,
)
from src.infrastructure.vector_stores.chroma.chroma_collection_factory import (  # noqa: E402
    get_or_create_chroma_collection,
)
from src.infrastructure.vector_stores.chroma.chroma_question_vector_store import (  # noqa: E402
    ChromaQuestionVectorStore,
)
from src.scripts.index_question_bank import index_question_bank  # noqa: E402

BANK = Path(__file__).resolve().parents[2] / "data/question_bank/questions.json"
DIM = 16


class HashEmbedder:
    """Deterministic bag-of-words embedder; identical text -> identical vector."""

    def _vector(self, text: str) -> list[float]:
        vec = [0.0] * DIM
        for word in text.lower().split():
            digest = hashlib.sha256(word.encode()).digest()
            vec[digest[0] % DIM] += 1.0
        norm = sum(v * v for v in vec) ** 0.5 or 1.0
        return [v / norm for v in vec]

    def embed_text(self, *, text: str) -> list[float]:
        return self._vector(text)

    def embed_many(self, *, texts: list[str]) -> list[list[float]]:
        return [self._vector(text) for text in texts]


def _run(tmp_path: Path, bank: Path):
    return index_question_bank(
        bank_path=bank,
        persist_directory=str(tmp_path / "chroma"),
        collection_name="questions",
        embedding_provider=HashEmbedder(),
    )


def _store(tmp_path: Path) -> ChromaQuestionVectorStore:
    collection = get_or_create_chroma_collection(
        client=create_chroma_client(persist_directory=str(tmp_path / "chroma")),
        collection_name="questions",
    )
    return ChromaQuestionVectorStore(collection=collection)


def test_indexes_every_question_and_is_idempotent(tmp_path: Path) -> None:
    expected = len(json.loads(BANK.read_text(encoding="utf-8")))

    assert len(_run(tmp_path, BANK)) == expected
    assert len(_run(tmp_path, BANK)) == expected  # re-run upserts, no duplicates

    store = _store(tmp_path)
    assert store._collection.count() == expected


def test_exact_question_text_is_top_hit(tmp_path: Path) -> None:
    questions = _run(tmp_path, BANK)
    target = next(q for q in questions if q.id == "rag_jr_001")

    results = _store(tmp_path).search_questions(
        query_embedding=HashEmbedder().embed_text(text=target.text),
        top_k=3,
    )

    assert results, "search returned nothing"
    assert results[0].question.id == target.id


def test_level_filter_is_applied(tmp_path: Path) -> None:
    _run(tmp_path, BANK)

    results = _store(tmp_path).search_questions(
        query_embedding=HashEmbedder().embed_text(text="design a production system"),
        top_k=10,
        filters=SearchFilters(level=Level.SENIOR),
    )

    assert results
    assert {str(r.question.level) for r in results} == {"SENIOR"}


def test_questions_removed_from_bank_are_pruned(tmp_path: Path) -> None:
    _run(tmp_path, BANK)

    records = json.loads(BANK.read_text(encoding="utf-8"))[:5]
    smaller = tmp_path / "small_bank.json"
    smaller.write_text(json.dumps(records), encoding="utf-8")
    _run(tmp_path, smaller)

    assert _store(tmp_path)._collection.count() == 5
