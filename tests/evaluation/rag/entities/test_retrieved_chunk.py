from __future__ import annotations

import pytest

from src.evaluation.rag.entities.retrieved_chunk import RetrievedChunk


def test_retrieved_chunk_should_store_chunk_metadata() -> None:
    chunk = RetrievedChunk(chunk_id="c1", chunk_text="RAG context", document_id="doc1", source_name="docs", rank=1, score=0.9)
    assert chunk.chunk_id == "c1"
    assert chunk.document_id == "doc1"
    assert chunk.score == 0.9


def test_retrieved_chunk_should_reject_empty_chunk_text() -> None:
    with pytest.raises(ValueError):
        RetrievedChunk(chunk_id="c1", chunk_text="")
