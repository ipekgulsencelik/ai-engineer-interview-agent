from __future__ import annotations

from src.domain.validators.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.rag.entities.retrieved_chunk import (
    RetrievedChunk,
)
from src.evaluation.rag.schemas.chunk_attribution_request_schema import (
    CHUNK_ATTRIBUTION_REQUEST_SCHEMA,
)


class ChunkAttributionRequestValidator:
    """
    ChunkAttributionRequest validation service.
    """

    @staticmethod
    def validate(
        *,
        question: str,
        generated_answer: str,
        retrieved_chunks: tuple[
            RetrievedChunk,
            ...,
        ],
        model_name: str | None,
        evaluator_name: str | None,
        notes: str | None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "question": question,
                "generated_answer": generated_answer,
                "retrieved_chunks": retrieved_chunks,
                "model_name": model_name,
                "evaluator_name": evaluator_name,
                "notes": notes,
            },
            schema=CHUNK_ATTRIBUTION_REQUEST_SCHEMA,
            error_factory=EvaluationValidationError,
        )

        if not retrieved_chunks:
            raise EvaluationValidationError(
                "retrieved_chunks cannot be empty."
            )

        for index, chunk in enumerate(
            retrieved_chunks,
        ):
            if not isinstance(
                chunk,
                RetrievedChunk,
            ):
                raise EvaluationValidationError(
                    f"retrieved_chunks[{index}] must be RetrievedChunk."
                )