from __future__ import annotations

from typing import Final

from src.infrastructure.embedding.embedding_retry_executor import (
    EmbeddingRetryExecutor,
)
from src.infrastructure.embedding.sentence_transformer_embedding_provider import (
    SentenceTransformerEmbeddingProvider,
)
from src.infrastructure.embedding.sentence_transformer_model_loader import (
    SentenceTransformerModelLoader,
)

DEFAULT_EMBEDDING_MODEL_NAME: Final[str] = "all-MiniLM-L6-v2"
DEFAULT_RETRY_COUNT: Final[int] = 2
DEFAULT_RETRY_BACKOFF_SECONDS: Final[float] = 1.0
DEFAULT_BATCH_SIZE: Final[int] = 32


class SentenceTransformerEmbeddingProviderFactory:
    """
    Builds the default sentence-transformers embedding provider.

    The model is loaded (and downloaded on first use) when build() is called.
    """

    @staticmethod
    def build(
        *,
        model_name: str = DEFAULT_EMBEDDING_MODEL_NAME,
        normalize_embeddings: bool = True,
        batch_size: int = DEFAULT_BATCH_SIZE,
    ) -> SentenceTransformerEmbeddingProvider:
        return SentenceTransformerEmbeddingProvider(
            model=SentenceTransformerModelLoader.load(model_name=model_name),
            retry_executor=EmbeddingRetryExecutor(
                retry_count=DEFAULT_RETRY_COUNT,
                retry_backoff_seconds=DEFAULT_RETRY_BACKOFF_SECONDS,
            ),
            normalize_embeddings=normalize_embeddings,
            batch_size=batch_size,
        )
