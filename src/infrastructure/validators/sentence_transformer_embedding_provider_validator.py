from __future__ import annotations

from src.infrastructure.schemas.sentence_transformer_embedding_provider_schema import (
    SENTENCE_TRANSFORMER_EMBEDDING_PROVIDER_SCHEMA,
)
from src.infrastructure.validation.base_schema_validator import (
    BaseSchemaValidator,
)


class SentenceTransformerEmbeddingProviderValidator:
    """
    SentenceTransformer embedding provider validation facade.
    """

    @staticmethod
    def validate_model_name(
        model_name: str | None,
    ) -> None:
        BaseSchemaValidator.validate_optional_string(
            field_name="model_name",
            value=model_name,
            rules=SENTENCE_TRANSFORMER_EMBEDDING_PROVIDER_SCHEMA[
                "model_name"
            ],
        )

    @staticmethod
    def validate_text(
        text: str,
    ) -> str:
        return BaseSchemaValidator.validate_string_and_return(
            field_name="text",
            value=text,
            rules=SENTENCE_TRANSFORMER_EMBEDDING_PROVIDER_SCHEMA[
                "text"
            ],
        )

    @staticmethod
    def validate_texts(
        texts: list[str],
    ) -> list[str]:
        return BaseSchemaValidator.validate_string_list_and_return(
            field_name="texts",
            value=texts,
            rules=SENTENCE_TRANSFORMER_EMBEDDING_PROVIDER_SCHEMA[
                "texts"
            ],
        )

    @staticmethod
    def validate_retry_count(
        retry_count: int,
    ) -> None:
        BaseSchemaValidator.validate_numeric(
            field_name="retry_count",
            value=retry_count,
            rules=SENTENCE_TRANSFORMER_EMBEDDING_PROVIDER_SCHEMA[
                "retry_count"
            ],
        )

    @staticmethod
    def validate_retry_backoff_seconds(
        retry_backoff_seconds: float,
    ) -> None:
        BaseSchemaValidator.validate_numeric(
            field_name="retry_backoff_seconds",
            value=retry_backoff_seconds,
            rules=SENTENCE_TRANSFORMER_EMBEDDING_PROVIDER_SCHEMA[
                "retry_backoff_seconds"
            ],
        )

    @staticmethod
    def validate_batch_size(
        batch_size: int,
    ) -> None:
        BaseSchemaValidator.validate_numeric(
            field_name="batch_size",
            value=batch_size,
            rules=SENTENCE_TRANSFORMER_EMBEDDING_PROVIDER_SCHEMA[
                "batch_size"
            ],
        )

    @staticmethod
    def validate_normalize_embeddings(
        normalize_embeddings: bool,
    ) -> None:
        BaseSchemaValidator.validate_type(
            field_name="normalize_embeddings",
            value=normalize_embeddings,
            rules=SENTENCE_TRANSFORMER_EMBEDDING_PROVIDER_SCHEMA[
                "normalize_embeddings"
            ],
        )