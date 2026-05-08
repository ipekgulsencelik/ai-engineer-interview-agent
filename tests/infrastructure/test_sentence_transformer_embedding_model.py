import pytest

from src.infrastructure.embedding.sentence_transformer_embedding_model import (
    SentenceTransformerEmbeddingModel,
)


def test_embedding_model_generates_embedding() -> None:
    model = SentenceTransformerEmbeddingModel()

    embedding = model.embed("What is Retrieval-Augmented Generation?")

    assert isinstance(embedding, list)
    assert len(embedding) > 0


def test_embedding_model_batch_embedding() -> None:
    model = SentenceTransformerEmbeddingModel()

    embeddings = model.embed_batch(
        [
            "What is RAG?",
            "How do embeddings work?",
        ]
    )

    assert len(embeddings) == 2
    assert isinstance(embeddings[0], list)


def test_embedding_model_empty_text_raises_error() -> None:
    model = SentenceTransformerEmbeddingModel()

    with pytest.raises(
        ValueError,
        match="Text cannot be empty",
    ):
        model.embed("")


def test_embedding_model_empty_batch_raises_error() -> None:
    model = SentenceTransformerEmbeddingModel()

    with pytest.raises(
        ValueError,
        match="Texts cannot be empty",
    ):
        model.embed_batch([])
