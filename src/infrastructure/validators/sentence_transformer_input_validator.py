from __future__ import annotations

from src.infrastructure.validations.sentence_transformer_input_schema import (
    SentenceTransformerBatchTextSchema,
    SentenceTransformerTextSchema,
)


class SentenceTransformerInputValidator:
    """Validation facade over schema objects for sentence-transformer inputs."""

    @staticmethod
    def validate_text(text: str) -> str:
        return SentenceTransformerTextSchema.parse(text).text

    @staticmethod
    def validate_texts(texts: list[str]) -> list[str]:
        return SentenceTransformerBatchTextSchema.parse(texts).texts
