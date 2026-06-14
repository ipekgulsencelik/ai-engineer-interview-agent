from __future__ import annotations

from src.evaluation.rag.value_objects.chunk_attribution_result import (
    ChunkAttributionResult,
)


class ChunkAttributionResultFactory:
    """
    Factory for ChunkAttributionResult.
    """

    @staticmethod
    def create(
        *,
        chunk,
        attribution_score: float,
        chunk_token_count: int,
        matched_tokens: int,
    ) -> ChunkAttributionResult:
        return ChunkAttributionResult(
            chunk_id=chunk.chunk_id,
            document_id=chunk.document_id,
            source_name=chunk.source_name,
            attribution_score=attribution_score,
            supports_answer=(
                matched_tokens > 0
            ),
            chunk_token_count=chunk_token_count,
            matched_tokens=matched_tokens,
            matched_text=None,
            explanation=None,
            notes=None,
        )