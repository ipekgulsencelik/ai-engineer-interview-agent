from __future__ import annotations

from dataclasses import dataclass

from src.evaluation.rag.validators.retrieved_chunk_validator import RetrievedChunkValidator


@dataclass(frozen=True, slots=True, kw_only=True)
class RetrievedChunk:
    """Retrieved context chunk used for chunk attribution evaluation."""

    chunk_id: str
    chunk_text: str
    document_id: str | None = None
    source_name: str | None = None
    rank: int | None = None
    score: float | None = None

    def __post_init__(self) -> None:
        RetrievedChunkValidator.validate(
            chunk_id=self.chunk_id,
            chunk_text=self.chunk_text,
            document_id=self.document_id,
            source_name=self.source_name,
            rank=self.rank,
            score=self.score,
        )
