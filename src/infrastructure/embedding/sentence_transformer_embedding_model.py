from __future__ import annotations

from src.application.ports.embedding_provider import EmbeddingProvider
from src.infrastructure.validators.sentence_transformer_embedding_provider_validator import (
    SentenceTransformerEmbeddingProviderValidator,
)

class SentenceTransformerEmbeddingProvider(EmbeddingProvider):
    """Sentence-transformers based embedding provider."""

    def __init__(self, model_name: str | None = None, model: object | None = None) -> None:
        SentenceTransformerEmbeddingProviderValidator.validate_model_name(model_name)

        if model is not None:
            self._model = model
            return

        from sentence_transformers import SentenceTransformer
        from src.config.settings import settings

        self._model = SentenceTransformer(model_name or settings.EMBEDDING_MODEL_NAME)

    def embed_text(self, text: str) -> list[float]:
        normalized = SentenceTransformerEmbeddingProviderValidator.validate_text(text)

        embedding = self._model.encode(normalized, normalize_embeddings=True)
        return embedding.tolist()

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        normalized_texts = SentenceTransformerEmbeddingProviderValidator.validate_texts(texts)
        embeddings = self._model.encode(normalized_texts, normalize_embeddings=True)
        return [embedding.tolist() for embedding in embeddings]