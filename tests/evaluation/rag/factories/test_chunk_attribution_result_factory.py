from __future__ import annotations

from src.evaluation.rag.entities.retrieved_chunk import RetrievedChunk
from src.evaluation.rag.factories.chunk_attribution_result_factory import ChunkAttributionResultFactory


def test_chunk_attribution_result_factory_should_copy_chunk_metadata_and_support_flag() -> None:
    result = ChunkAttributionResultFactory.create(
        chunk=RetrievedChunk(chunk_id="c1", chunk_text="rag context", document_id="d1", source_name="docs"),
        attribution_score=0.5,
        chunk_token_count=2,
        matched_tokens=1,
    )

    assert result.chunk_id == "c1"
    assert result.document_id == "d1"
    assert result.source_name == "docs"
    assert result.supports_answer is True
