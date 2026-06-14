from __future__ import annotations

from dataclasses import dataclass

from src.evaluation.rag.validators.chunk_attribution_result_validator import (
    ChunkAttributionResultValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ChunkAttributionResult:
    """
    Immutable chunk attribution result.

    Represents whether a retrieved chunk contributed
    to supporting a generated answer in a RAG evaluation.
    """

    chunk_id: str

    attribution_score: float

    supports_answer: bool

    chunk_token_count: int

    matched_tokens: int

    document_id: str | None = None

    source_name: str | None = None

    matched_text: str | None = None

    explanation: str | None = None

    notes: str | None = None

    def __post_init__(
        self,
    ) -> None:
        ChunkAttributionResultValidator.validate(
            chunk_id=self.chunk_id,
            attribution_score=self.attribution_score,
            supports_answer=self.supports_answer,
            chunk_token_count=self.chunk_token_count,
            matched_tokens=self.matched_tokens,
            document_id=self.document_id,
            source_name=self.source_name,
            matched_text=self.matched_text,
            explanation=self.explanation,
            notes=self.notes,
        )

    @property
    def is_attributed(
        self,
    ) -> bool:
        return self.supports_answer

    @property
    def has_match(
        self,
    ) -> bool:
        return self.matched_text is not None

    @property
    def has_explanation(
        self,
    ) -> bool:
        return self.explanation is not None

    @property
    def attribution_ratio(
        self,
    ) -> float:
        if self.chunk_token_count == 0:
            return 0.0

        return (
            self.matched_tokens
            / self.chunk_token_count
        )