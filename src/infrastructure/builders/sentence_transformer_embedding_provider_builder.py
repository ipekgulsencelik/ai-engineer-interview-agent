from __future__ import annotations

from src.config.settings import settings
from src.infrastructure.constants.embedding_defaults import (
    DEFAULT_BATCH_SIZE,
    DEFAULT_NORMALIZE_EMBEDDINGS,
    DEFAULT_RETRY_BACKOFF_SECONDS,
    DEFAULT_RETRY_COUNT,
)
from src.infrastructure.embedding.embedding_retry_executor import (
    EmbeddingRetryExecutor,
)
from src.infrastructure.embedding.sentence_transformer_embedding_provider import (
    SentenceTransformerEmbeddingProvider,
)
from src.infrastructure.embedding.sentence_transformer_model_loader import (
    SentenceTransformerModelLoader,
)
from src.infrastructure.validators.sentence_transformer_embedding_provider_validator import (
    SentenceTransformerEmbeddingProviderValidator,
)


class SentenceTransformerEmbeddingProviderBuilder:
    """
    SentenceTransformerEmbeddingProvider dependency composition builder.
    """

    @staticmethod
    def build_default(
        *,
        model_name: str | None = None,
        normalize_embeddings: bool = DEFAULT_NORMALIZE_EMBEDDINGS,
        retry_count: int = DEFAULT_RETRY_COUNT,
        retry_backoff_seconds: float = DEFAULT_RETRY_BACKOFF_SECONDS,
        batch_size: int = DEFAULT_BATCH_SIZE,
    ) -> SentenceTransformerEmbeddingProvider:
        SentenceTransformerEmbeddingProviderBuilder._validate_config(
            model_name=model_name,
            normalize_embeddings=normalize_embeddings,
            retry_count=retry_count,
            retry_backoff_seconds=retry_backoff_seconds,
            batch_size=batch_size,
        )

        resolved_model_name = (
            model_name
            or settings.EMBEDDING_MODEL_NAME
        )

        SentenceTransformerEmbeddingProviderValidator.validate_model_name(
            resolved_model_name,
        )

        model = SentenceTransformerModelLoader.load(
            model_name=resolved_model_name,
        )

        retry_executor = EmbeddingRetryExecutor(
            retry_count=retry_count,
            retry_backoff_seconds=retry_backoff_seconds,
        )

        return SentenceTransformerEmbeddingProvider(
            model=model,
            retry_executor=retry_executor,
            normalize_embeddings=normalize_embeddings,
            batch_size=batch_size,
        )

    @staticmethod
    def _validate_config(
        *,
        model_name: str | None,
        normalize_embeddings: bool,
        retry_count: int,
        retry_backoff_seconds: float,
        batch_size: int,
    ) -> None:
        SentenceTransformerEmbeddingProviderValidator.validate_model_name(
            model_name,
        )
        SentenceTransformerEmbeddingProviderValidator.validate_normalize_embeddings(
            normalize_embeddings,
        )
        SentenceTransformerEmbeddingProviderValidator.validate_retry_count(
            retry_count,
        )
        SentenceTransformerEmbeddingProviderValidator.validate_retry_backoff_seconds(
            retry_backoff_seconds,
        )
        SentenceTransformerEmbeddingProviderValidator.validate_batch_size(
            batch_size,
        )