from __future__ import annotations

from src.domain.validators.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.rag.schemas.retrieval_hit_rate_request_schema import (
    RETRIEVAL_HIT_RATE_REQUEST_SCHEMA,
)


class RetrievalHitRateRequestValidator:
    """
    RetrievalHitRateRequest validation service.
    """

    @staticmethod
    def validate(
        *,
        question: str,
        expected_chunk_id: str,
        retrieved_chunk_ids: tuple[
            str,
            ...,
        ],
        top_k: int,
        expected_context: str | None,
        retrieved_contexts: tuple[
            str,
            ...,
        ],
        model_name: str | None,
        retriever_name: str | None,
        notes: str | None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "question": question,
                "expected_chunk_id": expected_chunk_id,
                "retrieved_chunk_ids": retrieved_chunk_ids,
                "top_k": top_k,
                "expected_context": expected_context,
                "retrieved_contexts": retrieved_contexts,
                "model_name": model_name,
                "retriever_name": retriever_name,
                "notes": notes,
            },
            schema=RETRIEVAL_HIT_RATE_REQUEST_SCHEMA,
            error_factory=EvaluationValidationError,
        )

        for index, chunk_id in enumerate(
            retrieved_chunk_ids,
        ):
            if not isinstance(
                chunk_id,
                str,
            ) or not chunk_id.strip():
                raise EvaluationValidationError(
                    f"retrieved_chunk_ids[{index}] must be non-empty string."
                )

        for index, context in enumerate(
            retrieved_contexts,
        ):
            if not isinstance(
                context,
                str,
            ) or not context.strip():
                raise EvaluationValidationError(
                    f"retrieved_contexts[{index}] must be non-empty string."
                )

        if top_k == 0:
            raise EvaluationValidationError(
                "top_k must be greater than zero."
            )

        if len(
            retrieved_chunk_ids,
        ) > top_k:
            raise EvaluationValidationError(
                "retrieved_chunk_ids cannot exceed top_k."
            )

        if (
            retrieved_contexts
            and len(retrieved_contexts)
            != len(retrieved_chunk_ids)
        ):
            raise EvaluationValidationError(
                "retrieved_contexts length must match retrieved_chunk_ids length."
            )