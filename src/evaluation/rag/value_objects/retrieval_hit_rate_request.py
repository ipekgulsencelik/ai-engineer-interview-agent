from __future__ import annotations

from dataclasses import dataclass

from src.evaluation.rag.validators.retrieval_hit_rate_request_validator import (
    RetrievalHitRateRequestValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class RetrievalHitRateRequest:
    """
    Request model for retrieval hit-rate evaluation.

    Represents the inputs required to determine
    whether retrieval successfully returned
    at least one relevant context.
    """

    question: str

    expected_chunk_id: str

    retrieved_chunk_ids: tuple[
        str,
        ...
    ]

    top_k: int

    expected_context: str | None = None

    retrieved_contexts: tuple[
        str,
        ...,
    ] = ()

    model_name: str | None = None

    retriever_name: str | None = None

    notes: str | None = None

    def __post_init__(
        self,
    ) -> None:
        RetrievalHitRateRequestValidator.validate(
            question=self.question,
            expected_chunk_id=self.expected_chunk_id,
            retrieved_chunk_ids=self.retrieved_chunk_ids,
            top_k=self.top_k,
            expected_context=self.expected_context,
            retrieved_contexts=self.retrieved_contexts,
            model_name=self.model_name,
            retriever_name=self.retriever_name,
            notes=self.notes,
        )