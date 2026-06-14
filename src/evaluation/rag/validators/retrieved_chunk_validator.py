from __future__ import annotations

from src.domain.validators.schema_validator import SchemaValidator
from src.evaluation.domain.errors.evaluation_validation_error import EvaluationValidationError
from src.evaluation.rag.schemas.retrieved_chunk_schema import RETRIEVED_CHUNK_SCHEMA


class RetrievedChunkValidator:
    """Validates retrieved chunk value objects."""

    @staticmethod
    def validate(
        *,
        chunk_id: str,
        chunk_text: str,
        document_id: str | None,
        source_name: str | None,
        rank: int | None,
        score: float | None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "chunk_id": chunk_id,
                "chunk_text": chunk_text,
                "document_id": document_id,
                "source_name": source_name,
                "rank": rank,
                "score": score,
            },
            schema=RETRIEVED_CHUNK_SCHEMA,
            error_factory=EvaluationValidationError,
        )
