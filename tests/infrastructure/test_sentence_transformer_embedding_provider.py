from dataclasses import dataclass

import pytest

from src.infrastructure.embedding.sentence_transformer_embedding_provider import (
    SentenceTransformerEmbeddingProvider,
)


@dataclass
class _FakeVector:
    value: list[float]

    def tolist(self) -> list[float]:
        return self.value


@dataclass
class FakeSentenceTransformer:
    def encode(self, text_or_texts, normalize_embeddings: bool = True):
        if isinstance(text_or_texts, str):
            return _FakeVector([float(len(text_or_texts))])
        return [_FakeVector([float(len(t))]) for t in text_or_texts]


def test_embed_text_delegates_to_model_encode() -> None:
    provider = SentenceTransformerEmbeddingProvider(model=FakeSentenceTransformer())

    assert provider.embed_text("hello") == [5.0]


def test_embed_batch_delegates_to_model_encode() -> None:
    provider = SentenceTransformerEmbeddingProvider(model=FakeSentenceTransformer())

    assert provider.embed_batch(["hi", "hello"]) == [[2.0], [5.0]]


def test_embed_text_rejects_empty_input() -> None:
    provider = SentenceTransformerEmbeddingProvider(model=FakeSentenceTransformer())

    with pytest.raises(ValueError, match="text cannot be empty"):
        provider.embed_text("   ")
