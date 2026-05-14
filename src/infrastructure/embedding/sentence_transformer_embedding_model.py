from __future__ import annotations

import logging
import time
from typing import Any

from sentence_transformers import SentenceTransformer

from src.config.settings import settings
from src.infrastructure.validators.sentence_transformer_input_validator import (
    SentenceTransformerInputValidator,
)
from src.interfaces.embedding_model import EmbeddingModel

logger = logging.getLogger(__name__)


class SentenceTransformerEmbeddingModel(EmbeddingModel):
    """Sentence-transformers based embedding model with validation + retry."""

    def __init__(
        self,
        model_name: str | None = None,
        *,
        normalize_embeddings: bool = True,
        retry_count: int = 2,
        retry_backoff_seconds: float = 0.25,
        batch_size: int = 32,
    ) -> None:
        self.model_name = model_name or settings.EMBEDDING_MODEL_NAME
        self.normalize_embeddings = normalize_embeddings
        self.retry_count = retry_count
        self.retry_backoff_seconds = retry_backoff_seconds
        self.batch_size = batch_size
        self.model = SentenceTransformer(self.model_name)

    def embed(self, text: str) -> list[float]:
        cleaned_text = SentenceTransformerInputValidator.validate_text(text)
        embedding = self._encode_with_retry(cleaned_text)
        return embedding.tolist()

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        cleaned_texts = SentenceTransformerInputValidator.validate_texts(texts)
        embeddings = self._encode_with_retry(cleaned_texts)
        return [embedding.tolist() for embedding in embeddings]

    def _encode_with_retry(self, payload: str | list[str]) -> Any:
        last_error: Exception | None = None

        for attempt in range(1, self.retry_count + 2):
            try:
                return self.model.encode(
                    payload,
                    normalize_embeddings=self.normalize_embeddings,
                    batch_size=self.batch_size,
                    show_progress_bar=False,
                )
            except Exception as error:
                last_error = error
                logger.warning(
                    "Embedding encode failed (attempt %s/%s): %s",
                    attempt,
                    self.retry_count + 1,
                    error,
                )
                if attempt <= self.retry_count:
                    time.sleep(self.retry_backoff_seconds * attempt)

        raise RuntimeError("Failed to generate embeddings after retries.") from last_error