from __future__ import annotations

from src.evaluation.rag.entities.retrieved_chunk import RetrievedChunk
from src.evaluation.rag.evaluators.chunk_attribution_evaluator import ChunkAttributionEvaluator
from src.evaluation.rag.value_objects.chunk_attribution_request import ChunkAttributionRequest


def test_chunk_attribution_evaluator_should_score_each_retrieved_chunk() -> None:
    results = ChunkAttributionEvaluator().evaluate(
        request=ChunkAttributionRequest(
            question="q",
            generated_answer="rag context",
            retrieved_chunks=(
                RetrievedChunk(chunk_id="c1", chunk_text="rag context evidence"),
                RetrievedChunk(chunk_id="c2", chunk_text="unrelated text"),
            ),
        )
    )

    assert len(results) == 2
    assert results[0].chunk_id == "c1"
    assert results[0].attribution_score == 1.0
    assert results[0].supports_answer is True
    assert results[1].attribution_score == 0.0
    assert results[1].supports_answer is False
