from __future__ import annotations

from typing import Any

from src.application.ports.embedding_provider import (
    EmbeddingProvider,
)
from src.infrastructure.embedding.embedding_retry_executor import (
    EmbeddingRetryExecutor,
)
from src.infrastructure.validators.sentence_transformer_embedding_provider_validator import (
    SentenceTransformerEmbeddingProviderValidator,
)


class SentenceTransformerEmbeddingProvider(EmbeddingProvider):
    """
    Sentence-transformers based embedding provider.
    """

    def __init__(
        self,
        *,
        model: Any,
        retry_executor: EmbeddingRetryExecutor,
        normalize_embeddings: bool,
        batch_size: int,
    ) -> None:
        SentenceTransformerEmbeddingProviderValidator.validate_normalize_embeddings(
            normalize_embeddings,
        )
        SentenceTransformerEmbeddingProviderValidator.validate_batch_size(
            batch_size,
        )

        self._model = model
        self._retry_executor = retry_executor
        self._normalize_embeddings = normalize_embeddings
        self._batch_size = batch_size

    def embed_text(
        self,
        *,
        text: str,
    ) -> list[float]:
        normalized_text = (
            SentenceTransformerEmbeddingProviderValidator.validate_text(
                text,
            )
        )

        embedding = self._retry_executor.execute(
            model=self._model,
            payload=normalized_text,
            normalize_embeddings=self._normalize_embeddings,
            batch_size=self._batch_size,
        )

        return embedding.tolist()

    def embed_many(
        self,
        *,
        texts: list[str],
    ) -> list[list[float]]:
        normalized_texts = (
            SentenceTransformerEmbeddingProviderValidator.validate_texts(
                texts,
            )
        )

        embeddings = self._retry_executor.execute(
            model=self._model,
            payload=normalized_texts,
            normalize_embeddings=self._normalize_embeddings,
            batch_size=self._batch_size,
        )

        return [
            embedding.tolist()
            for embedding in embeddings
        ]