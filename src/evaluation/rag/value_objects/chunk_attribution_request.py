from __future__ import annotations

from dataclasses import dataclass

from src.evaluation.rag.entities.retrieved_chunk import (
    RetrievedChunk,
)
from src.evaluation.rag.validators.chunk_attribution_request_validator import (
    ChunkAttributionRequestValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ChunkAttributionRequest:
    """
    Request model for chunk attribution evaluation.

    Represents the inputs required to determine
    which retrieved chunks contributed evidence
    to the generated answer.
    """

    question: str

    generated_answer: str

    retrieved_chunks: tuple[
        RetrievedChunk,
        ...
    ]

    model_name: str | None = None

    evaluator_name: str | None = None

    notes: str | None = None

    def __post_init__(
        self,
    ) -> None:
        ChunkAttributionRequestValidator.validate(
            question=self.question,
            generated_answer=self.generated_answer,
            retrieved_chunks=self.retrieved_chunks,
            model_name=self.model_name,
            evaluator_name=self.evaluator_name,
            notes=self.notes,
        )