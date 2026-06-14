from __future__ import annotations

from src.domain.validation.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.rag.schemas.chunk_attribution_result_schema import (
    CHUNK_ATTRIBUTION_RESULT_SCHEMA,
)


class ChunkAttributionResultValidator:
    """
    ChunkAttributionResult validation service.
    """

    @staticmethod
    def validate(
        *,
        chunk_id: str,
        attribution_score: float,
        supports_answer: bool,
        chunk_token_count: int,
        matched_tokens: int,
        document_id: str | None,
        source_name: str | None,
        matched_text: str | None,
        explanation: str | None,
        notes: str | None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "chunk_id": chunk_id,
                "attribution_score": attribution_score,
                "supports_answer": supports_answer,
                "chunk_token_count": chunk_token_count,
                "matched_tokens": matched_tokens,
                "document_id": document_id,
                "source_name": source_name,
                "matched_text": matched_text,
                "explanation": explanation,
                "notes": notes,
            },
            schema=CHUNK_ATTRIBUTION_RESULT_SCHEMA,
            error_factory=EvaluationValidationError,
        )

        if matched_tokens > chunk_token_count:
            raise EvaluationValidationError(
                "matched_tokens cannot exceed chunk_token_count."
            )

        if (
            supports_answer
            and matched_tokens == 0
        ):
            raise EvaluationValidationError(
                "matched_tokens must be greater than zero when supports_answer is true."
            )