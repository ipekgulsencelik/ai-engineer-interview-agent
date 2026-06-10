from __future__ import annotations

from abc import ABC, abstractmethod


class EmbeddingModel(ABC):
    """Common contract for text embedding providers."""

    @abstractmethod
    def embed(self, text: str) -> list[float]:
        """
        Generate an embedding vector for a single text input.

        Args:
            text: Input text to embed.

        Returns:
            Embedding vector as a JSON-serializable list of floats.
        """
        raise NotImplementedError

    @abstractmethod
    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """
        Generate embedding vectors for multiple text inputs.

        Args:
            texts: List of input texts to embed.

        Returns:
            List of embedding vectors in the same order as input texts.
        """
        raise NotImplementedError