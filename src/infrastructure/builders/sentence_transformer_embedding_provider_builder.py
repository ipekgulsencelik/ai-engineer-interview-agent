from __future__ import annotations

from src.config.settings import settings
from src.infrastructure.embedding.embedding_retry_executor import (
    EmbeddingRetryExecutor,
)
from src.infrastructure.embedding.sentence_transformer_embedding_provider import (
    SentenceTransformerEmbeddingProvider,
)
from src.infrastructure.loaders.sentence_transformer_model_loader import (
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
        normalize_embeddings: bool = True,
        retry_count: int = 2,
        retry_backoff_seconds: float = 0.25,
        batch_size: int = 32,
    ) -> SentenceTransformerEmbeddingProvider:
        SentenceTransformerEmbeddingProviderValidator.validate_model_name(
            model_name,
        )

        resolved_model_name = (
            model_name
            or settings.EMBEDDING_MODEL_NAME
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