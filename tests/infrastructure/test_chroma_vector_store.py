from src.infrastructure.embedding.sentence_transformer_embedding_model import (
    SentenceTransformerEmbeddingModel,
)
from src.infrastructure.vector_stores.chroma_vector_store import (
    ChromaVectorStore,
)


def test_chroma_vector_store_add_and_search() -> None:
    embedding_model = SentenceTransformerEmbeddingModel()

    store = ChromaVectorStore(
        collection_name="test_collection",
        persist_directory="data/chroma_test",
    )

    question_text = "What is Retrieval-Augmented Generation?"

    embedding = embedding_model.embed(question_text)

    store.add(
        id="q1",
        text=question_text,
        metadata={
            "category": "RAG",
        },
        embedding=embedding,
    )

    query_embedding = embedding_model.embed("Explain RAG systems.")

    results = store.search(
        query_embedding=query_embedding,
        limit=1,
    )

    assert len(results) == 1
    assert results[0].id == "q1"
